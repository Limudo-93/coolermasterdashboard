#!/bin/bash
# TTS com voz echo (masculina) via OpenAI API
# Uso: tts-echo.sh "texto para falar" [output_path]

TEXT="$1"
OUTPUT="${2:-/tmp/jubinha_voice.opus}"
API_KEY="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"

curl -s https://api.openai.com/v1/audio/speech \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"gpt-4o-mini-tts\",
    \"input\": $(echo "$TEXT" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read().strip()))'),
    \"voice\": \"echo\",
    \"instructions\": \"Fale em português brasileiro, com tom natural e amigável. Você é o Jubinha, um assistente divertido.\",
    \"response_format\": \"opus\"
  }" \
  -o "$OUTPUT"

echo "$OUTPUT"
