'use client'

// This file MUST be completely standalone - no imports from app providers,
// no Tailwind classes, no context. Railway/Next.js 16 prerender requires isolation.
export default function GlobalError({
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <html lang="en">
      <head>
        <title>Something went wrong – ProjectMentor AI</title>
      </head>
      <body
        style={{
          margin: 0,
          padding: 0,
          backgroundColor: '#0b1220',
          color: '#e2e8f0',
          fontFamily: 'system-ui, -apple-system, sans-serif',
          display: 'flex',
          minHeight: '100vh',
          alignItems: 'center',
          justifyContent: 'center',
          textAlign: 'center',
        }}
      >
        <div style={{ padding: '2rem', maxWidth: '480px' }}>
          <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>⚠️</div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 700, marginBottom: '0.75rem' }}>
            Something went wrong
          </h2>
          <p style={{ color: '#94a3b8', marginBottom: '1.5rem', lineHeight: 1.6 }}>
            An unexpected error occurred while loading ProjectMentor AI. Please try again.
          </p>
          <button
            onClick={() => reset()}
            style={{
              backgroundColor: '#6366f1',
              color: '#ffffff',
              border: 'none',
              borderRadius: '0.5rem',
              padding: '0.625rem 1.5rem',
              fontSize: '0.875rem',
              fontWeight: 600,
              cursor: 'pointer',
            }}
          >
            Try again
          </button>
        </div>
      </body>
    </html>
  )
}
