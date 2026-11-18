import { useState } from 'react'
import {
  MODEL_CACHE,
  buildModelUrl,
  cacheKey,
  getModel,
  type ModelSpec,
} from '../../services/models/registry.js'
import type { ModelSource } from '../../services/settings.js'

export type ModelState = 'missing' | 'partial' | 'ready'

export type DownloadProgress = {
  /** 已完成字节 */
  done: number
  /** 总字节 */
  total: number
  /** 当前文件名 */
  current: string
}

const openCache = async (): Promise<Cache | null> => {
  if (typeof caches === 'undefined') {
    return null
  }
  return caches.open(MODEL_CACHE)
}

/** 模型是否已完整缓存 */
export const getModelState = async (
  model: ModelSpec,
  source: ModelSource
): Promise<ModelState> => {
  const cache = await openCache()
  if (!cache) {
    return 'missing'
  }
  let present = 0
  for (const file of model.files) {
    const hit = await cache.match(cacheKey(source, model.repo, file.path))
    if (hit) {
      present += 1
    }
  }
  if (present === 0) {
    return 'missing'
  }
  return present === model.files.length ? 'ready' : 'partial'
}

const totalBytes = (model: ModelSpec) =>
  model.files.reduce((sum, file) => sum + file.bytes, 0)

/**
 * 下载一个模型的全部文件到 CacheStorage。
 * 逐个文件流式读取并回报进度；中断时已完成的文件保留，可续传（重新下载只补缺失文件）。
 */
export const downloadModel = async (
  modelId: string,
  source: ModelSource,
  onProgress: (progress: DownloadProgress) => void,
  signal: AbortSignal
): Promise<void> => {
  const model = getModel(modelId)
  if (!model) {
    throw new Error(`unknown model: ${modelId}`)
  }
  if (source === 'manual') {
    throw new Error('manual source needs a local file import')
  }
  const cache = await openCache()
  if (!cache) {
    throw new Error('CacheStorage is not available')
  }
  const total = totalBytes(model)
  let done = 0
  for (const file of model.files) {
    if (signal.aborted) {
      return
    }
    const url = buildModelUrl(source, model.repo, file.path)
    const key = cacheKey(source, model.repo, file.path)
    if (await cache.match(key)) {
      done += file.bytes
      onProgress({ done, total, current: file.path })
      continue
    }
    onProgress({ done, total, current: file.path })
    const response = await fetch(url, { signal })
    if (!response.ok) {
      throw new Error(`${response.status} ${response.statusText}: ${url}`)
    }
    // 边读边写：用流式 Response 让 CacheStorage 存完整响应体
    await cache.put(key, response.clone())
    done += file.bytes
    onProgress({ done, total, current: file.path })
  }
}

/** 删除一个模型的所有缓存 */
export const deleteModel = async (modelId: string, source: ModelSource): Promise<void> => {
  const model = getModel(modelId)
  const cache = await openCache()
  if (!model || !cache) {
    return
  }
  for (const file of model.files) {
    await cache.delete(cacheKey(source, model.repo, file.path))
  }
}

/** 读取已缓存模型文件的原始字节（推理时用） */
export const readModelFile = async (
  modelId: string,
  path: string,
  source: ModelSource
): Promise<ArrayBuffer | null> => {
  const model = getModel(modelId)
  const cache = await openCache()
  if (!model || !cache) {
    return null
  }
  const hit = await cache.match(cacheKey(source, model.repo, path))
  return hit ? hit.arrayBuffer() : null
}

/** 组件用：订阅模型状态与下载进度 */
export const useModelRow = (modelId: string, source: ModelSource) => {
  const [state, setState] = useState<ModelState>('missing')
  const [progress, setProgress] = useState<DownloadProgress | null>(null)
  const [error, setError] = useState<string | null>(null)

  const refresh = async () => {
    const model = getModel(modelId)
    if (model) {
      setState(await getModelState(model, source))
    }
  }

  return { state, progress, error, setState, setProgress, setError, refresh }
}
