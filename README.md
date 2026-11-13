# Avalon

Avalon is a Claude Code plugin that gives a repository a lasting home for its rules, decisions, and design descriptions: a docs tree that an agent reads at the start of every session.

## Status

Avalon is a **pre-release**. This repo holds its planning documents and its own first docs tree. It holds **no working round table yet**, so the plugin you can install does nothing useful. Versions stay below 1.0 until that changes.

## Install

This repo is a Claude Code marketplace, and the plugin lives in its `plugin/` folder. Only that folder is installed. To add the marketplace and install the plugin, run:

```text
/plugin marketplace add stimothy/avalon
/plugin install avalon@avalon
```

To receive a later release, refresh the marketplace and update the plugin, then restart Claude Code:

```text
/plugin marketplace update avalon
/plugin update avalon@avalon
```

To try a local checkout, start Claude Code with `--plugin-dir ./plugin`.

## Privacy

Avalon collects no usage data and opens no network connection.

## Contributing

To set up the tools and run the tests, see [CONTRIBUTING.md](CONTRIBUTING.md). Everyone taking part is asked to follow the [code of conduct](CODE_OF_CONDUCT.md).

## Licence

Avalon is released under the [MIT licence](LICENSE).
