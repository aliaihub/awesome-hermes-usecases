# Self-Hosted Nextcloud Workspace Assistant

**Class:** Ecosystem integration · **Confidence:** Medium-High · **Demo status:** Runnable Hermes skill

## Pain Point

Teams and individuals who self-host Nextcloud still switch between browser tabs to manage files, notes, calendars, tasks, and contacts. General cloud-assistant integrations often require handing that data to an additional hosted service.

## What It Does

`hermes-nextcloud` installs as a Hermes productivity skill and wraps Nextcloud's standard interfaces in one command-line layer:

- WebDAV for listing, uploading, downloading, moving, and deleting files.
- Notes API for creating and editing notes.
- CalDAV for calendars, events, and Tasks calendars.
- CardDAV for browsing, searching, and exporting contacts.

Hermes can invoke these operations from its normal conversation surfaces while the data remains in the operator's Nextcloud instance.

## Setup

Create a revocable Nextcloud app password, then install and configure the skill:

```bash
cd ~/.hermes/skills/productivity
git clone https://github.com/adnw-vinc/hermes-nextcloud.git nextcloud

python3 ~/.hermes/skills/productivity/nextcloud/scripts/setup.py
```

The setup writes validated credentials to `~/.hermes/nextcloud.env`. Verify the connection with the documented CLI wrapper:

```bash
NC="python3 ~/.hermes/skills/productivity/nextcloud/scripts/nextcloud_api.py"
$NC check
```

## Prompts

Use conversation requests that map directly to the skill's documented operations:

```text
List the files in my Nextcloud project folder and summarize the newest notes.
```

```text
Show my Nextcloud calendar events and tasks for this week. Do not change anything.
```

## Skills Needed

- `hermes-nextcloud` productivity skill
- Python 3.8+
- A reachable Nextcloud instance
- Nextcloud app password
- Notes and Tasks apps when those operations are needed

## Notes

- The setup stores the app password in a mode-`0600` file. Use an app password rather than the account's main password so access can be revoked independently.
- Read-only requests are a safer starting point. Confirm targets before deleting or moving remote files, contacts, or events.
- Calendar timestamps use the configured timezone and otherwise default to UTC.

## Sources

- hermes-nextcloud repository: <https://github.com/adnw-vinc/hermes-nextcloud>
- Hermes Agent repository: <https://github.com/NousResearch/hermes-agent>

