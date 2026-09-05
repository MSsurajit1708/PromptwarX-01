'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { ArrowRight } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { ChipGroup } from '@/components/chip-group'
import { useStore } from '@/lib/store'
import {
  GOAL_OPTIONS,
  INTEREST_OPTIONS,
  LANGUAGE_OPTIONS,
  TIME_OPTIONS,
} from '@/lib/data'
import type { Profile, SkillLevel } from '@/lib/types'
import { cn } from '@/lib/utils'

const SKILL_LEVELS: { value: SkillLevel; label: string; hint: string }[] = [
  { value: 'beginner', label: 'Beginner', hint: 'New to building full projects' },
  { value: 'intermediate', label: 'Intermediate', hint: 'Comfortable, still leveling up' },
  { value: 'advanced', label: 'Advanced', hint: 'Ship complex things confidently' },
]

export function OnboardingForm() {
  const router = useRouter()
  const { profile: existing, setProfile } = useStore()

  const [skillLevel, setSkillLevel] = useState<SkillLevel>(existing?.skillLevel ?? 'intermediate')
  const [languages, setLanguages] = useState<string[]>(existing?.languages ?? [])
  const [interests, setInterests] = useState<string[]>(existing?.interests ?? [])
  const [goal, setGoal] = useState<string>(existing?.goal ?? '')
  const [timeCommitment, setTimeCommitment] = useState<string>(existing?.timeCommitment ?? '')
  const [experience, setExperience] = useState<string>(existing?.experience ?? '')

  const canSubmit = languages.length > 0 && interests.length > 0 && Boolean(goal) && Boolean(timeCommitment)

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!canSubmit) return
    const next: Profile = { skillLevel, languages, interests, goal, timeCommitment, experience }
    setProfile(next)
    router.push('/generate')
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-8">
      <fieldset className="space-y-3">
        <Label className="text-base">How would you rate your skill level?</Label>
        <div className="grid gap-3 sm:grid-cols-3">
          {SKILL_LEVELS.map((s) => {
            const active = skillLevel === s.value
            return (
              <button
                key={s.value}
                type="button"
                onClick={() => setSkillLevel(s.value)}
                aria-pressed={active}
                className={cn(
                  'rounded-xl border p-4 text-left transition-colors',
                  active
                    ? 'border-primary bg-primary/10'
                    : 'border-border bg-card hover:border-primary/40',
                )}
              >
                <p className="font-medium">{s.label}</p>
                <p className="mt-1 text-sm text-muted-foreground">{s.hint}</p>
              </button>
            )
          })}
        </div>
      </fieldset>

      <fieldset className="space-y-3">
        <Label className="text-base">Which languages and tools do you know?</Label>
        <ChipGroup options={LANGUAGE_OPTIONS} selected={languages} onChange={setLanguages} />
      </fieldset>

      <fieldset className="space-y-3">
        <Label className="text-base">What are you interested in building?</Label>
        <ChipGroup options={INTEREST_OPTIONS} selected={interests} onChange={setInterests} />
      </fieldset>

      <div className="grid gap-8 sm:grid-cols-2">
        <fieldset className="space-y-3">
          <Label className="text-base">What&apos;s your main goal?</Label>
          <ChipGroup options={GOAL_OPTIONS} selected={goal ? [goal] : []} onChange={(v) => setGoal(v[0] ?? '')} single />
        </fieldset>
        <fieldset className="space-y-3">
          <Label className="text-base">How much time do you have?</Label>
          <ChipGroup
            options={TIME_OPTIONS}
            selected={timeCommitment ? [timeCommitment] : []}
            onChange={(v) => setTimeCommitment(v[0] ?? '')}
            single
          />
        </fieldset>
      </div>

      <fieldset className="space-y-3">
        <Label htmlFor="experience" className="text-base">
          Anything else? <span className="font-normal text-muted-foreground">(optional)</span>
        </Label>
        <Textarea
          id="experience"
          value={experience}
          onChange={(e) => setExperience(e.target.value)}
          placeholder="e.g. I want to learn backend, I'm prepping for a frontend interview, I love CLIs..."
          rows={3}
        />
      </fieldset>

      <div className="flex items-center justify-between gap-4 border-t border-border pt-6">
        <p className="font-mono text-xs text-muted-foreground">
          {canSubmit ? 'Ready to generate ideas' : 'Pick a language, interest, goal, and time'}
        </p>
        <Button type="submit" size="lg" disabled={!canSubmit} className="gap-2">
          Generate ideas
          <ArrowRight className="size-4" />
        </Button>
      </div>
    </form>
  )
}
