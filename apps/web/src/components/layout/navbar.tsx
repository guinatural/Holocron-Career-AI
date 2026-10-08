import Link from 'next/link'
import { Button } from '@/components/ui/button'

export function Navbar() {
  return (
    <div className="w-full flex flex-col font-sans">
      {/* Top Utility Bar (Dark) */}
      <div className="bg-[#232F3E] text-white/90 text-[12px] py-2 px-6 flex justify-end gap-6 font-medium">
        <span className="hover:text-white cursor-pointer flex items-center gap-1">🌐 Português</span>
        <span className="hover:text-white cursor-pointer">Entre em contato conosco</span>
        <span className="hover:text-white cursor-pointer">Marketplace</span>
        <span className="hover:text-white cursor-pointer">Suporte</span>
        <span className="hover:text-white cursor-pointer">Minha conta</span>
      </div>

      {/* Main Navbar (Light) */}
      <nav className="bg-white border-b border-gray-200 px-6 py-3 flex items-center justify-between sticky top-0 z-50">
        <div className="flex items-center gap-8">
          <Link href="/" className="flex items-center gap-2">
            <span className="text-2xl font-black tracking-tighter text-[#232F3E]">
              holocron
            </span>
          </Link>
          <div className="hidden md:flex gap-6 text-[14px] font-medium text-gray-700">
            <Link href="/console" className="hover:text-[#FF9900] transition-colors">Descubra os Agentes</Link>
            <Link href="/produtos" className="hover:text-[#FF9900] transition-colors">Produtos</Link>
            <Link href="/solucoes" className="hover:text-[#FF9900] transition-colors">Soluções</Link>
            <Link href="/precos" className="hover:text-[#FF9900] transition-colors">Preços</Link>
            <Link href="/recursos" className="hover:text-[#FF9900] transition-colors">Recursos</Link>
          </div>
        </div>
        
        <div className="flex items-center gap-6">
          <span className="text-sm text-gray-700 font-medium cursor-pointer hover:text-black flex items-center gap-1">
            🔍 Pesquisar
          </span>
          <span className="text-sm text-gray-700 font-medium cursor-pointer hover:text-black hidden sm:block">
            Faça login no console
          </span>
          <Button className="bg-[#232F3E] hover:bg-[#1a232e] text-white rounded-full px-6 font-semibold h-10 shadow-none">
            Criar conta
          </Button>
        </div>
      </nav>
    </div>
  )
}
