import Link from 'next/link'
import { Button } from '@/components/ui/button'

export function Navbar() {
  return (
    <nav className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="flex h-14 items-center px-4 max-w-7xl mx-auto">
        <div className="mr-4 flex">
          <Link href="/" className="mr-6 flex items-center space-x-2">
            <span className="hidden font-bold sm:inline-block">
              Holocron Career AI
            </span>
          </Link>
          <div className="flex gap-4 text-sm font-medium">
            <Link href="/dashboard" className="transition-colors hover:text-foreground/80 text-foreground">
              Dashboard
            </Link>
            <Link href="/agentes" className="transition-colors hover:text-foreground/80 text-foreground/60">
              Meus Agentes
            </Link>
            <Link href="/vagas" className="transition-colors hover:text-foreground/80 text-foreground/60">
              Vagas
            </Link>
          </div>
        </div>
        <div className="flex flex-1 items-center justify-between space-x-2 md:justify-end">
          <Button variant="ghost" size="sm">Log in</Button>
          <Button size="sm">Sign up</Button>
        </div>
      </div>
    </nav>
  )
}
