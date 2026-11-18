import { useEffect, useState, type ReactNode } from 'react'
import clsx from 'clsx'
import { Select } from '../base/Select.js'
import { showToast } from '../base/toastState.js'
import { useTranslate } from '../../i18n/index.js'
import {
  DEFAULT_API_BASE_URL,
  resolveSystemPrompt,
  setApiBaseUrl,
  setAsrEngine,
  setFontScale,
  setImageApiKey,
  setImageBaseUrl,
  setImageEnabled,
  setImageModel,
  setSearch,
  setSendSafetyCheck,
  setSamplingParam,
  setSkin,
  setThemeAuto,
  setSystemPrompt,
  setThinking,
  setTtsRate,
  setTtsSystemVoice,
  setTtsVoice,
  setUiMode,
  useSettings,
  type AsrEngine,
  type UiMode,
} from '../../services/settings.js'
import { isThemeId, THEMES } from '../../app/themes/registry.js'
import type { ThemeId } from '../../app/themes/types.js'
import { SettingCell } from './SettingCell.js'
import { CharacterCardSetting } from './CharacterCardSetting.js'
import styles from './Ext.module.css'

/** 带保存按钮的单行输入 */
const SaveField = ({
  label,
  description,
  value,
  placeholder,
  type = 'text',
  onSave,
  extra,
}: {
  label: string
  description?: string
  value: string
  placeholder?: string
  type?: 'text' | 'password'
  onSave: (next: string) => void
  extra?: ReactNode
}) => {
  const t = useTranslate()
  const [draft, setDraft] = useState(value)
  useEffect(() => setDraft(value), [value])
  const dirty = draft !== value
  return (
    <SettingCell
      label={label}
      description={description}
      status={null}
      stacked
      action={
        <div className={styles.fieldRow}>
          <input
            className={styles.input}
            type={type}
            value={draft}
            placeholder={placeholder}
            autoComplete="off"
            spellCheck={false}
            onChange={(event) => setDraft(event.target.value)}
          />
          {extra}
          <button
            type="button"
            className={clsx(styles.saveButton, !dirty && styles.saveButtonIdle)}
            disabled={!dirty}
            onClick={() => {
              onSave(draft.trim())
              showToast(t('odsSaved'))
            }}
          >
            {t('odsSave')}
          </button>
        </div>
      }
    />
  )
}

const ModeSetting = () => {
  const t = useTranslate()
  const uiMode = useSettings((state) => state.uiMode)
  return (
    <SettingCell
      label={t('odsMode')}
      description={t('odsModeHint')}
      status={null}
      action={
        <Select<UiMode>
          ariaLabel={t('odsMode')}
          value={uiMode}
          options={[
            { value: 'lite', label: t('odsModeLite') },
            { value: 'plus', label: t('odsModePlus') },
          ]}
          onChange={setUiMode}
        />
      }
    />
  )
}

const ApiBaseUrlSetting = () => {
  const t = useTranslate()
  const apiBaseUrl = useSettings((state) => state.apiBaseUrl)
  return (
    <SaveField
      label={t('odsApiBaseUrl')}
      description={t('odsApiBaseUrlHint')}
      value={apiBaseUrl}
      placeholder={DEFAULT_API_BASE_URL}
      onSave={setApiBaseUrl}
    />
  )
}

const SystemPromptSetting = () => {
  const t = useTranslate()
  const systemPrompt = useSettings((state) => state.systemPrompt)
  const [draft, setDraft] = useState(systemPrompt)
  useEffect(() => setDraft(systemPrompt), [systemPrompt])
  return (
    <SettingCell
      label={t('odsSystemPrompt')}
      description={t('odsSystemPromptHint')}
      status={null}
      stacked
      action={
        <div className={styles.column}>
          <textarea
            className={styles.textarea}
            value={draft}
            rows={5}
            placeholder={resolveSystemPrompt()}
            onChange={(event) => setDraft(event.target.value)}
          />
          <div className={styles.buttonRow}>
            <button
              type="button"
              className={styles.saveButton}
              onClick={() => {
                setSystemPrompt(draft)
                showToast(t('odsSaved'))
              }}
            >
              {t('odsSave')}
            </button>
            <button
              type="button"
              className={styles.ghostButton}
              onClick={() => {
                setSystemPrompt('')
                setDraft('')
                showToast(t('odsSaved'))
              }}
            >
              {t('odsReset')}
            </button>
          </div>
        </div>
      }
    />
  )
}

const DefaultToggleSettings = () => {
  const t = useTranslate()
  const thinking = useSettings((state) => state.thinking)
  const search = useSettings((state) => state.search)
  return (
    <>
      <SettingCell
        label={t('odsDefaultThinking')}
        description={t('odsDefaultThinkingHint')}
        status={null}
        action={
          <button
            type="button"
            role="switch"
            aria-checked={thinking}
            className={clsx(styles.switch, thinking && styles.switchOn)}
            onClick={() => setThinking(!thinking)}
          >
            <span className={styles.switchThumb} />
          </button>
        }
      />
      <SettingCell
        label={t('odsDefaultSearch')}
        description={t('odsDefaultSearchHint')}
        status={null}
        action={
          <button
            type="button"
            role="switch"
            aria-checked={search}
            className={clsx(styles.switch, search && styles.switchOn)}
            onClick={() => setSearch(!search)}
          >
            <span className={styles.switchThumb} />
          </button>
        }
      />
    </>
  )
}

/** 生成参数：安全档位与采样直调（Plus 用） */
const GenerationSettings = () => {
  const t = useTranslate()
  const sendSafetyCheck = useSettings((state) => state.sendSafetyCheck)
  const temperature = useSettings((state) => state.temperature)
  const topP = useSettings((state) => state.topP)
  const maxOutputTokens = useSettings((state) => state.maxOutputTokens)

  const numberRow = (
    key: 'temperature' | 'topP' | 'maxOutputTokens',
    label: string,
    hint: string,
    value: number | null,
    placeholder: string
  ) => (
    <SettingCell
      label={label}
      description={hint}
      status={null}
      action={
        <input
          className={styles.input}
          type="number"
          inputMode="decimal"
          step={key === 'topP' ? 0.01 : key === 'temperature' ? 0.05 : 1}
          min={0}
          max={key === 'topP' ? 1 : key === 'temperature' ? 2 : undefined}
          placeholder={placeholder}
          defaultValue={value ?? ''}
          onBlur={(event) => {
            const raw = event.target.value.trim()
            const next = raw === '' ? null : Number(raw)
            setSamplingParam(key, next !== null && Number.isFinite(next) ? next : null)
          }}
        />
      }
    />
  )

  return (
    <div className={styles.group}>
      <div className={styles.groupTitle}>{t('odsGenerationTitle')}</div>
      <SettingCell
        label={t('odsSafetyCheck')}
        description={t('odsSafetyCheckHint')}
        status={null}
        action={
          <button
            type="button"
            role="switch"
            aria-checked={sendSafetyCheck}
            className={clsx(styles.switch, sendSafetyCheck && styles.switchOn)}
            onClick={() => setSendSafetyCheck(!sendSafetyCheck)}
          >
            <span className={styles.switchThumb} />
          </button>
        }
      />
      {numberRow('temperature', t('odsTemperature'), t('odsTemperatureHint'), temperature, '1')}
      {numberRow('topP', t('odsTopP'), t('odsTopPHint'), topP, '1')}
      {numberRow('maxOutputTokens', t('odsMaxTokens'), t('odsMaxTokensHint'), maxOutputTokens, t('odsParamUnset'))}
    </div>
  )
}

const AppearanceSettings = () => {
  const t = useTranslate()
  const skin = useSettings((state) => state.skin)
  const themeAuto = useSettings((state) => state.themeAuto)
  const fontScale = useSettings((state) => state.fontScale)
  return (
    <>
      <SettingCell
        label={t('odsTheme')}
        description={t('odsThemeHint')}
        status={null}
        action={
          <Select<ThemeId>
            ariaLabel={t('odsTheme')}
            value={isThemeId(skin) ? skin : 'plain'}
            options={THEMES.map((item) => ({
              value: item.id,
              label: t(item.nameKey),
            }))}
            onChange={setSkin}
          />
        }
      />
      <SettingCell
        label={t('odsThemeAuto')}
        description={t('odsThemeAutoHint')}
        status={null}
        action={
          <button
            type="button"
            role="switch"
            aria-checked={themeAuto}
            className={clsx(styles.switch, themeAuto && styles.switchOn)}
            onClick={() => setThemeAuto(!themeAuto)}
          >
            <span className={styles.switchThumb} />
          </button>
        }
      />
      <SettingCell
        label={t('odsFontScale')}
        status={null}
        action={
          <Select<string>
            ariaLabel={t('odsFontScale')}
            value={String(fontScale)}
            options={[
              { value: '0.9', label: t('odsFontSmall') },
              { value: '1', label: t('odsFontStandard') },
              { value: '1.15', label: t('odsFontLarge') },
              { value: '1.3', label: t('odsFontHuge') },
            ]}
            onChange={(value) => setFontScale(Number(value))}
          />
        }
      />
    </>
  )
}

const TtsFineTuning = () => {
  const t = useTranslate()
  const engine = useSettings((state) => state.ttsEngine)
  const rate = useSettings((state) => state.ttsRate)
  const systemVoice = useSettings((state) => state.ttsSystemVoice)
  const cloudVoice = useSettings((state) => state.ttsVoice)
  const [voices, setVoices] = useState<SpeechSynthesisVoice[]>([])

  useEffect(() => {
    if (!('speechSynthesis' in window)) {
      return
    }
    const load = () => {
      const all = window.speechSynthesis.getVoices()
      setVoices(all.filter((voice) => voice.lang.toLowerCase().startsWith('zh')))
    }
    load()
    window.speechSynthesis.addEventListener('voiceschanged', load)
    return () => window.speechSynthesis.removeEventListener('voiceschanged', load)
  }, [])

  return (
    <>
      <SettingCell
        label={t('odsTtsRate')}
        description={t('odsTtsRateHint', { rate: rate.toFixed(1) })}
        status={null}
        stacked
        action={
          <input
            className={styles.range}
            type="range"
            min={0.5}
            max={2}
            step={0.1}
            value={rate}
            aria-label={t('odsTtsRate')}
            onChange={(event) => setTtsRate(Number(event.target.value))}
          />
        }
      />
      {engine === 'system' ? (
        <SettingCell
          label={t('odsTtsSystemVoice')}
          description={t('odsTtsSystemVoiceHint')}
          status={null}
          action={
            <Select<string>
              ariaLabel={t('odsTtsSystemVoice')}
              value={systemVoice}
              options={[
                { value: '', label: t('odsTtsSystemVoiceAuto') },
                ...voices.map((voice) => ({ value: voice.name, label: voice.name })),
              ]}
              onChange={(value) => setTtsSystemVoice(value)}
            />
          }
        />
      ) : null}
      {engine === 'cloud' ? (
        <SettingCell
          label={t('odsTtsCloudVoice')}
          description={t('odsTtsCloudVoiceHint')}
          status={null}
          action={
            <Select<string>
              ariaLabel={t('odsTtsCloudVoice')}
              value={cloudVoice}
              options={[
                { value: 'stella', label: t('settingsTtsVoiceStella') },
                { value: 'tide', label: t('settingsTtsVoiceTide') },
              ]}
              onChange={(value) => setTtsVoice(value === 'tide' ? 'tide' : 'stella')}
            />
          }
        />
      ) : null}
    </>
  )
}

const VoiceSettings = () => {
  const t = useTranslate()
  const asrEngine = useSettings((state) => state.asrEngine)
  return (
    <>
      <SettingCell
        label={t('odsAsrEngine')}
        description={t('odsAsrEngineHint')}
        status={null}
        action={
          <Select<AsrEngine>
            ariaLabel={t('odsAsrEngine')}
            value={asrEngine}
            options={[
              { value: 'system', label: t('odsAsrSystem') },
              { value: 'local', label: t('odsAsrLocal') },
              { value: 'cloud', label: t('odsAsrCloud') },
            ]}
            onChange={setAsrEngine}
          />
        }
      />
      <TtsFineTuning />
    </>
  )
}

const ImageSettings = () => {
  const t = useTranslate()
  const imageEnabled = useSettings((state) => state.imageEnabled)
  const imageBaseUrl = useSettings((state) => state.imageBaseUrl)
  const imageApiKey = useSettings((state) => state.imageApiKey)
  const imageModel = useSettings((state) => state.imageModel)
  return (
    <>
      <SettingCell
        label={t('odsImageEnabled')}
        description={t('odsImageHint')}
        status={null}
        action={
          <button
            type="button"
            role="switch"
            aria-checked={imageEnabled}
            className={clsx(styles.switch, imageEnabled && styles.switchOn)}
            onClick={() => setImageEnabled(!imageEnabled)}
          >
            <span className={styles.switchThumb} />
          </button>
        }
      />
      {imageEnabled ? (
        <>
          <SaveField
            label={t('odsImageBaseUrl')}
            value={imageBaseUrl}
            placeholder="https://api.openai.com/v1"
            onSave={setImageBaseUrl}
          />
          <SaveField
            label={t('odsImageApiKey')}
            value={imageApiKey}
            type="password"
            onSave={setImageApiKey}
          />
          <SaveField
            label={t('odsImageModel')}
            value={imageModel}
            placeholder="gpt-image-1"
            onSave={setImageModel}
          />
        </>
      ) : null}
    </>
  )
}

/** 设置里的「扩展」分组：模式、服务地址、提示词、外观、语音与算力、生图 */
export const ExtSettings = () => (
  <>
    <ModeSetting />
    <DefaultToggleSettings />
    <GenerationSettings />
    <ApiBaseUrlSetting />
    <SystemPromptSetting />
    <CharacterCardSetting />
    <AppearanceSettings />
    <VoiceSettings />
    <ImageSettings />
  </>
)
