import type { Difficulty } from './types'

export function difficultyClasses(difficulty: Difficulty) {
  switch (difficulty) {
    case 'Beginner':
      return 'border-chart-2/40 bg-chart-2/10 text-chart-2'
    case 'Intermediate':
      return 'border-chart-3/40 bg-chart-3/10 text-chart-3'
    case 'Advanced':
      return 'border-chart-4/40 bg-chart-4/10 text-chart-4'
  }
}

export function priorityClasses(priority: 'Must-have' | 'Nice-to-have' | 'Stretch') {
  switch (priority) {
    case 'Must-have':
      return 'border-primary/40 bg-primary/10 text-primary'
    case 'Nice-to-have':
      return 'border-chart-2/40 bg-chart-2/10 text-chart-2'
    case 'Stretch':
      return 'border-border bg-muted text-muted-foreground'
  }
}
