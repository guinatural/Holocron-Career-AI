import Link from 'next/link'

export default function ConsoleLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-[calc(100vh-60px)] w-full bg-slate-50/50 font-sans">
      {/* Sidebar global do Console */}
      <aside className="w-64 border-r bg-white flex flex-col hidden md:flex">
        <div className="h-14 flex items-center border-b px-6">
          <span className="font-bold text-[#232F3E] text-sm uppercase tracking-wider">Painel de Controle</span>
        </div>
        <nav className="flex-1 py-6 px-3 space-y-2">
          <Link href="/console" className="flex items-center px-3 py-2 text-[#4a5568] hover:bg-[#f0f4f8] hover:text-[#1a202c] rounded-md font-medium text-sm transition-colors">
            Dashboard
          </Link>
          <Link href="/console/vagas" className="flex items-center px-3 py-2 text-[#4a5568] hover:bg-[#f0f4f8] hover:text-[#1a202c] rounded-md font-medium text-sm transition-colors">
            Vagas Alvo
          </Link>
          <Link href="/console/agentes" className="flex items-center px-3 py-2 text-[#4a5568] hover:bg-[#f0f4f8] hover:text-[#1a202c] rounded-md font-medium text-sm transition-colors">
            Meus Agentes
          </Link>
          <Link href="/console/perfil" className="flex items-center px-3 py-2 text-[#4a5568] hover:bg-[#f0f4f8] hover:text-[#1a202c] rounded-md font-medium text-sm transition-colors">
            Meu Perfil (Upload)
          </Link>
        </nav>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <header className="h-14 flex items-center justify-end border-b bg-white px-8">
          <div className="flex items-center gap-4">
            <span className="text-sm font-medium text-[#4a5568]">guilherme@holocron.ai</span>
            <div className="w-8 h-8 rounded-full bg-[#232F3E] flex items-center justify-center text-white font-bold text-sm shadow-sm">
              GB
            </div>
          </div>
        </header>
        <main className="flex-1 overflow-auto">
            {children}
        </main>
      </div>
    </div>
  )
}
