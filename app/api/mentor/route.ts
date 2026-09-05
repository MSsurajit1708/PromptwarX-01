import {
  convertToModelMessages,
  createUIMessageStreamResponse,
  streamText,
  toUIMessageStream,
  type UIMessage,
} from 'ai'
import { MODEL } from '@/lib/schemas'

export const maxDuration = 60

export async function POST(req: Request) {
  const { messages, context }: { messages: UIMessage[]; context?: string } = await req.json()

  const system = [
    'You are ProjectMentor, a warm but direct senior engineering mentor.',
    'Help the developer actually build and ship their project. Give concrete, specific advice, not platitudes.',
    'When useful, suggest exact next steps, name real tools/libraries, and flag common pitfalls.',
    'Keep answers focused and skimmable. Use short paragraphs or tight bullet lists. Avoid unnecessary preamble.',
    context ? `\nThe developer is working on this project:\n${context}` : '',
  ]
    .filter(Boolean)
    .join(' ')

  const result = streamText({
    model: MODEL,
    system,
    messages: await convertToModelMessages(messages),
  })

  return createUIMessageStreamResponse({
    stream: toUIMessageStream({ stream: result.stream }),
  })
}
