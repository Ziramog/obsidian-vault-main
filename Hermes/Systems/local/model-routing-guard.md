# Local Hermes model-routing guard

## Desired state

- All local profiles use `opencode-go` / `deepseek-v4.1-flash`.
- Exception: `algolab-strategy` uses `openai-codex` / `gpt-5.6-sol`.
- Exact mapping lives in `model-routing-baseline.json`; it contains no credentials.

## Enforcement

`scripts/hermes-model-routing-guard.sh` reads each profile's effective `model.provider` and `model.default` through Hermes CLI. On drift, it restores only those two keys through `hermes -p <profile> config set`.

It never reads or writes `.env`, `auth.json`, fallbacks, MoA presets, aliases or auxiliary model settings.

Logs are outside the vault:

`C:\Users\ingju\AppData\Local\hermes\model-routing-guard\logs\`

## Account-change rule

Changing the OpenAI/Codex account must use the provider authentication flow, not `hermes model` or `hermes setup`. Those interactive selectors can rewrite the selected provider/default model.

After any account change, run the guard manually or wait for its scheduled run.

## Scheduled tasks

- `HermesModelRoutingGuard-Logon` — at user logon.
- `HermesModelRoutingGuard-Hourly` — every hour.

Both run the same guard. The guard is idempotent: when configuration matches baseline, it performs only read checks and writes no config.
