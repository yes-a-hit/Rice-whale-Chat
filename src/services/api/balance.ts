import { getApiOrigin } from './client.js'
import { useSettings } from '../settings.js'

/**
 * 余额查询：DeepSeek 官方 `GET /user/balance`。
 * BYOK 场景下用户真正关心的是「还剩多少钱」，所以放在数据管理里一眼能看到。
 */

export type BalanceInfo = {
  currency: string
  total_balance: string
  granted_balance?: string
  topped_up_balance?: string
}

export type Balance = {
  is_available: boolean
  balance_infos: BalanceInfo[]
}

export class BalanceError extends Error {}

export const fetchBalance = async (signal?: AbortSignal): Promise<Balance> => {
  const apiKey = useSettings.getState().apiKey
  if (!apiKey) {
    throw new BalanceError('no api key')
  }
  const response = await fetch(`${getApiOrigin()}/user/balance`, {
    headers: { Authorization: `Bearer ${apiKey}`, Accept: 'application/json' },
    signal,
  })
  if (!response.ok) {
    throw new BalanceError(`HTTP ${response.status}`)
  }
  const payload = (await response.json()) as Balance
  if (!payload || !Array.isArray(payload.balance_infos)) {
    throw new BalanceError('unexpected response')
  }
  return payload
}

/** 把余额信息压成一行展示文本 */
export const formatBalance = (balance: Balance): string => {
  if (balance.balance_infos.length === 0) {
    return '—'
  }
  return balance.balance_infos
    .map((info) => {
      const symbol = info.currency === 'USD' ? '$' : info.currency === 'CNY' ? '¥' : `${info.currency} `
      return `${symbol}${info.total_balance}`
    })
    .join(' / ')
}
