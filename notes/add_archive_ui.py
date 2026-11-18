import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- SessionItem：菜单加归档 ----------
p = root / "src/components/sider/SessionItem.tsx"
t = io.open(p, encoding="utf-8").read()
if "archiveSession" not in t:
    t = t.replace(
        "import { renameSession, selectSession } from '../../services/chat/store.js'",
        "import { archiveSession, renameSession, selectSession } from '../../services/chat/store.js'\n"
        "import { IconArchiveOutline16 } from '../base/icons.js'",
        1,
    )
    t = t.replace(
        """            {
              key: 'delete',""",
        """            {
              key: 'archive',
              label: session.archived ? t('odsUnarchive') : t('odsArchive'),
              icon: <IconArchiveOutline16 />,
              onSelect: () => archiveSession(session.id, !session.archived),
            },
            {
              key: 'delete',""",
        1,
    )
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("session item ok")

# ---------- Sider：已归档筛选 ----------
p = root / "src/components/sider/Sider.tsx"
t = io.open(p, encoding="utf-8").read()
if "showArchived" not in t:
    t = t.replace(
        "  const groups = useMemo(() => groupSessions(sessions, now, t), [sessions, now, t])",
        """  const [showArchived, setShowArchived] = useState(false)
  // 默认只看未归档；打开「已归档」时反过来只看归档的
  const visibleSessions = useMemo(
    () => sessions.filter((session) => Boolean(session.archived) === showArchived),
    [sessions, showArchived]
  )
  const groups = useMemo(() => groupSessions(visibleSessions, now, t), [visibleSessions, now, t])""",
        1,
    )
    t = t.replace(
        """      <div className={styles.bottom}>
        <button type="button" className={styles.settings} onClick={() => openSettings('general')}>""",
        """      <div className={styles.bottom}>
        <button
          type="button"
          className={styles.settings}
          onClick={() => setShowArchived((value) => !value)}
        >
          <span className={styles.settingsIcon}>{showArchived ? 'π' : 'ϟ'}</span>
          <span className={styles.settingsLabel}>
            {showArchived ? t('odsBackToChats') : t('odsArchivedChats')}
          </span>
        </button>
        <button type="button" className={styles.settings} onClick={() => openSettings('general')}>""",
        1,
    )
    if "useState" not in t:
        t = t.replace("import { useEffect, useMemo", "import { useEffect, useMemo, useState", 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("sider ok")
