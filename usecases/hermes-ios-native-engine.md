# Hermes iOS Native Engine

**Class:** Mobile companion · **Confidence:** High · **Demo status:** Public community project

## Pain Point

Desktop and server Hermes sessions miss the context that lives on a phone:
camera input, voice, location, activity, health metrics, widgets, and mobile
notifications. Browser or chat frontends can send messages, but they do not
expose native iOS sensors or a self-hosted phone-to-Hermes control plane.

## What It Does

Hermes iOS is a self-hosted iPhone companion for a user-owned Hermes runtime. It
adds a native iOS app, a relay, and a host-side connector so Hermes can move
between desktop, phone, sensors, voice, widgets, and local agent tools.

The connector stores phone context locally and exposes it to Hermes through MCP
tools. Current capabilities include:

- Streaming chat with attachments, retries, markdown, and inline returned
  images.
- Voice mode with camera context and Hermes tool delegation.
- Dynamic slash-command catalog sourced from Hermes built-ins, skills,
  personalities, and quick commands.
- GPS location, reverse-geocoded addresses, activity, and HealthKit metrics.
- Home Screen widgets, Live Activities, and host/model/context status.
- Self-hosted relay and connector pairing flow.

## Setup

Run the relay, pair the iPhone app with the connector, and point the connector
at the local Hermes runtime. The project provides separate app, relay, and
connector components.

Example connector-side usage after setup:

```text
Hermes reads sensor data from the local connector SQLite database through the
bundled MCP server.
```

For physical devices, use a LAN IP or public URL for the relay. `localhost` on
the phone points back to the phone, not the Hermes host.

## Prompts

Use phone context:

```text
Use my latest location and activity data to plan a realistic evening errand
route. Do not send messages or create calendar events without approval.
```

Health dashboard:

```text
Query the available iOS sensor metrics for the past 30 days and build a local
markdown summary with step, sleep, and heart-rate trends.
```

Camera-assisted workflow:

```text
Use the latest camera attachment from Hermes iOS to identify the device model
and draft setup notes for it.
```

## Skills Needed

- Hermes iOS app, relay, and host connector
- `hermes_mobile` MCP tools
- Optional: OpenAI Realtime for voice mode
- iOS permissions for Health, location, motion, camera, and notifications as
  needed

## Notes

- The project is independent and community-built, not an official Nous Research
  component.
- The privacy posture depends on self-hosting the relay and connector. Sensor
  data should stay local unless the user deliberately exposes it.
- This complements the existing Android control use case. Android focuses on
  remote device automation; Hermes iOS focuses on native companion context and
  sensor-aware workflows.

## Sources

- Hermes iOS repository: <https://github.com/dylan-buck/Hermes-iOS>
