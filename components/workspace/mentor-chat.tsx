'use client'

import { useEffect, useMemo, useRef, useState } from 'react'
import { useChat } from '@ai-sdk/react'
import { DefaultChatTransport, type UIMessage } from 'ai'
import { ArrowUp, Sparkles } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { useStore } from '@/lib/store'
import { cn } from '@/lib/utils'
import type { ChatMessage, Project } from '@/lib/types'

function buildContext(project: Project): string {
  const { idea, plan } = project
  const lines = [
    `Title: ${idea.title} — ${idea.tagline}`,
    `Description: ${idea.description}`,
    `Difficulty: ${idea.difficulty}, ~${idea.estimatedWeeks} weeks, domain ${idea.domain}.`,
  ]
  if (plan) {
    lines.push(`Roadmap phases: ${plan.roadmap.map((p) => p.title).join(', ')}.`)
    lines.push(`Must-have features: ${plan.features.filter((f) => f.priority === 'Must-have').map((f) => f.title).join(', ')}.`)
    lines.push(`Recommended stack: ${[...plan.techStack.frontend, ...plan.techStack.backend, ...plan.techStack.data].map((t) => t.name).join(', ')}.`)
  }
  return lines.join('\n')
}

const STARTERS = [
  'What should I build first?',
  'What are the trickiest parts of this?',
  'Suggest a folder structure to start.',
]

function partsToText(message: UIMessage): string {
  return message.parts
    .map((p) => (p.type === 'text' ? p.text : ''))
    .join('')
}

export function MentorChat({ project }: { project: Project }) {
  const { addMentorMessage } = useStore()
  const context = useMemo(() => buildContext(project), [project])

  const initialMessages = useMemo<UIMessage[]>(
    () =>
      project.mentorMessages.map((m) => ({
        id: m.id,
        role: m.role,
        parts: [{ type: 'text', text: m.content }],
      })),
    // Only seed once on mount.
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [],
  )

  const { messages, sendMessage, status } = useChat({
    messages: initialMessages,
    transport: new DefaultChatTransport({ api: '/api/mentor', body: { context } }),
  })

  const [input, setInput] = useState('')
  const scrollRef = useRef<HTMLDivElement>(null)
  const persistedIds = useRef(new Set(project.mentorMessages.map((m) => m.id)))

  // Persist any new completed messages to the store.
  useEffect(() => {
    if (status !== 'ready') return
    for (const m of messages) {
      if (persistedIds.current.has(m.id)) continue
      const text = partsToText(m)
      if (!text) continue
      persistedIds.current.add(m.id)
      addMentorMessage(project.id, { id: m.id, role: m.role as ChatMessage['role'], content: text })
    }
  }, [messages, status, addMentorMessage, project.id])

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: 'smooth' })
  }, [messages, status])

  function submit(text: string) {
    const trimmed = text.trim()
    if (!trimmed || status !== 'ready') return
    sendMessage({ text: trimmed })
    setInput('')
  }

  const busy = status === 'submitted' || status === 'streaming'

  return (
    <div className="flex h-[min(70vh,640px)] flex-col rounded-xl border border-border bg-card">
      <div ref={scrollRef} className="flex-1 space-y-4 overflow-y-auto p-4 sm:p-6">
        {messages.length === 0 ? (
          <div className="flex h-full flex-col items-center justify-center text-center">
            <div className="grid size-11 place-items-center rounded-xl border border-primary/30 bg-primary/10 text-primary">
              <Sparkles className="size-5" />
            </div>
            <h3 className="mt-4 font-semibold">Ask your mentor</h3>
            <p className="mt-1 max-w-sm text-sm text-muted-foreground">
              Your mentor already knows this project&apos;s plan. Ask about architecture, tricky decisions, or what to do next.
            </p>
            <div className="mt-5 flex flex-wrap justify-center gap-2">
              {STARTERS.map((s) => (
                <button
                  key={s}
                  onClick={() => submit(s)}
                  className="rounded-full border border-border bg-background px-3 py-1.5 text-sm text-muted-foreground transition-colors hover:border-primary/40 hover:text-foreground"
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        ) : (
          messages.map((m) => (
            <div key={m.id} className={cn('flex gap-3', m.role === 'user' && 'flex-row-reverse')}>
              <div
                className={cn(
                  'grid size-7 shrink-0 place-items-center rounded-md font-mono text-[11px]',
                  m.role === 'user'
                    ? 'bg-secondary text-secondary-foreground'
                    : 'bg-primary text-primary-foreground',
                )}
              >
                {m.role === 'user' ? 'You' : 'M'}
              </div>
              <div
                className={cn(
                  'max-w-[80%] whitespace-pre-wrap rounded-xl px-4 py-2.5 text-sm leading-relaxed',
                  m.role === 'user'
                    ? 'bg-secondary text-secondary-foreground'
                    : 'border border-border bg-background',
                )}
              >
                {partsToText(m) || (busy ? '…' : '')}
              </div>
            </div>
          ))
        )}
        {status === 'submitted' && (
          <div className="flex gap-3">
            <div className="grid size-7 shrink-0 place-items-center rounded-md bg-primary font-mono text-[11px] text-primary-foreground">
              M
            </div>
            <div className="rounded-xl border border-border bg-background px-4 py-2.5">
              <span className="inline-flex gap-1">
                <span className="size-1.5 animate-bounce rounded-full bg-muted-foreground [animation-delay:-0.3s]" />
                <span className="size-1.5 animate-bounce rounded-full bg-muted-foreground [animation-delay:-0.15s]" />
                <span className="size-1.5 animate-bounce rounded-full bg-muted-foreground" />
              </span>
            </div>
          </div>
        )}
      </div>

      <form
        onSubmit={(e) => {
          e.preventDefault()
          submit(input)
        }}
        className="flex items-center gap-2 border-t border-border p-3"
      >
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey && !e.nativeEvent.isComposing && e.keyCode !== 229) {
              e.preventDefault()
              submit(input)
            }
          }}
          placeholder="Ask your mentor anything about this project…"
          className="flex-1 bg-transparent px-2 text-sm outline-none placeholder:text-muted-foreground"
        />
        <Button type="submit" size="icon" disabled={busy || !input.trim()}>
          <ArrowUp className="size-4" />
          <span className="sr-only">Send</span>
        </Button>
      </form>
    </div>
  )
}
