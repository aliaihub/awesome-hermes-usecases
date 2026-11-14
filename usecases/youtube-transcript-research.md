# YouTube Transcripts and Search

<!-- catalog-summary:start -->
[← Browse use cases](../README.md#knowledge--research) · **Knowledge & Research**

| At a glance | Details |
| --- | --- |
| **Outcome** | YouTube transcripts with timestamps, video search, and channel and playlist browsing from a Hermes conversation. |
| **Requires** | GetYouTubeTranscript plugin; API key set as YOUTUBE_TRANSCRIPT_API_KEY; account credits per request. |
| **Available** | Plugin |
| **Validation** | Sources linked below; workflow not run during this submission. |
<!-- catalog-summary:end -->

**Class:** Ecosystem integration · **Confidence:** Medium · **Demo status:** Docs + runbook

## Pain Point

A Hermes agent asked about a YouTube video has no way to read what was said in
it. Pasting a transcript in by hand does not scale to a whole channel or
playlist, and the agent cannot find the right video to read in the first place.

## What It Does

The plugin connects Hermes to the GetYouTubeTranscript remote MCP server
(Streamable HTTP, `https://getyoutubetranscript.com/api/mcp`). The agent can
fetch a video's transcript with optional timestamps, search YouTube, and browse
a channel's videos and playlists. The plugin lists these read-only tools:
`get_youtube_transcript`, `get_transcript_languages`, `search_youtube`,
`list_channel_videos`, `search_channel_videos`, `get_channel_latest_videos`,
`list_channel_playlists`, `list_playlist_videos`, `get_related_videos` and
`get_credits`.

It also ships four skills that tell the agent when to use which tool:
`fetch-transcript`, `search-youtube`, `summarize-video` and
`channel-playlist-research`. The package is configuration (`plugin.json`,
`mcp.json`) and Markdown skills only. No local code runs.

## Setup

Install the plugin without enabling it, then enable it:

```bash
hermes plugins install tubeagentkit/youtube-transcript-hermes-plugin --no-enable
hermes plugins enable getyoutubetranscript
```

Create an API key in the GetYouTubeTranscript dashboard and set it as
`YOUTUBE_TRANSCRIPT_API_KEY` in your shell or in the profile `.env`. The plugin
sends it to the MCP server as a bearer token. Pricing: free account with 100
credits (one-time), paid plans from $5/month.

## Prompts

```text
Fetch the transcript of this video with timestamps and list the main
sections: <video URL>
```

```text
Search YouTube for recent talks on <topic>, then summarize the two most
relevant videos from their transcripts.
```

```text
List the playlists on this channel and pull the transcripts of the videos in
the first one: <channel URL>
```

## Skills Needed

- Hermes plugin system
- `getyoutubetranscript` plugin (MCP server `youtube-transcript` and four skills)
- GetYouTubeTranscript API key

## Notes

- Every tool call goes to `getyoutubetranscript.com`, which receives the video
  URL or search text and your API key.
- Transcript fetches use account credits.
- The tool set is served by the remote server at runtime, so it is not covered
  by a pinned commit.
- Transcripts are text written by whoever uploaded the video. The skills tell
  the agent to treat them as data, never as instructions.
- The author of this entry is the developer of the plugin.

## Sources

- Plugin repository: <https://github.com/tubeagentkit/youtube-transcript-hermes-plugin>
- Plugin README: <https://github.com/tubeagentkit/youtube-transcript-hermes-plugin#readme>
- Hosted MCP server and tool documentation: <https://github.com/tubeagentkit/youtube-mcp>
- API documentation: <https://getyoutubetranscript.com/docs>
