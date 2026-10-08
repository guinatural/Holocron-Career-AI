import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import Link from 'next/link'

export default function ConsoleDashboard() {
  return (
    <div className="flex min-h-[calc(100vh-60px)] w-full bg-slate-50/50 font-sans">
      {/* Sidebar */}
      <aside className="w-64 border-r bg-white flex flex-col">
        <div className="h-14 flex items-center border-b px-6">
          <span className="font-bold text-[#232F3E] text-sm uppercase tracking-wider">Painel de Controle</span>
        </div>
        <nav className="flex-1 py-6 px-3 space-y-2">
          <Link href="/console" className="flex items-center px-3 py-2 bg-[#f0f4f8] text-[#1a202c] rounded-md font-medium text-sm">
            Dashboard
          </Link>
          <Link href="/console/vagas" className="flex items-center px-3 py-2 text-[#4a5568] hover:bg-[#f0f4f8] hover:text-[#1a202c] rounded-md font-medium text-sm transition-colors">
            Vagas Alvo
          </Link>
          <Link href="/console/agentes" className="flex items-center px-3 py-2 text-[#4a5568] hover:bg-[#f0f4f8] hover:text-[#1a202c] rounded-md font-medium text-sm transition-colors">
            Meus Agentes
          </Link>
          <Link href="/console/perfil" className="flex items-center px-3 py-2 text-[#4a5568] hover:bg-[#f0f4f8] hover:text-[#1a202c] rounded-md font-medium text-sm transition-colors">
            Meu Perfil
          </Link>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col overflow-hidden">
        <header className="h-14 flex items-center justify-between border-b bg-white px-8">
          <h1 className="text-lg font-bold text-[#1a202c]">Visão Geral</h1>
          <div className="flex items-center gap-4">
            <span className="text-sm font-medium text-[#4a5568]">guilherme@holocron.ai</span>
            <div className="w-8 h-8 rounded-full bg-[#232F3E] flex items-center justify-center text-white font-bold text-sm shadow-sm">
              GB
            </div>
          </div>
        </header>

        <div className="flex-1 overflow-auto p-8 space-y-8">
          {/* Metrics Grid */}
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
            <Card className="shadow-sm border-gray-200">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-semibold text-[#4a5568]">Vagas Analisadas</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-black text-[#1a202c]">14</div>
                <p className="text-xs text-emerald-600 font-medium mt-1">+2 desde ontem</p>
              </CardContent>
            </Card>
            <Card className="shadow-sm border-gray-200">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-semibold text-[#4a5568]">Aplicações Ativas</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-black text-[#1a202c]">6</div>
                <p className="text-xs text-[#4a5568] font-medium mt-1">3 em fase de entrevista</p>
              </CardContent>
            </Card>
            <Card className="shadow-sm border-gray-200">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-semibold text-[#4a5568]">Score Médio (ATS)</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-black text-[#FF9900]">84%</div>
                <p className="text-xs text-[#4a5568] font-medium mt-1">Alta probabilidade de match</p>
              </CardContent>
            </Card>
            <Card className="shadow-sm border-gray-200">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-semibold text-[#4a5568]">Interações de IA</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-black text-[#1a202c]">89</div>
                <p className="text-xs text-[#4a5568] font-medium mt-1">Total de tokens gerados</p>
              </CardContent>
            </Card>
          </div>

          {/* Status Section */}
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-7">
            <Card className="col-span-4 shadow-sm border-gray-200">
              <CardHeader>
                <CardTitle className="text-[#1a202c]">Monitor de Agentes</CardTitle>
                <CardDescription>
                  Acompanhe os agentes autônomos trabalhando no seu perfil em tempo real.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="flex items-center border-l-4 border-emerald-500 pl-4 py-1">
                  <div className="space-y-1">
                    <p className="text-[15px] font-bold text-[#1a202c]">Scout Agent (Pesquisa)</p>
                    <p className="text-sm text-[#4a5568]">Buscando vagas em Next.js e AWS Cloud...</p>
                  </div>
                  <div className="ml-auto">
                    <span className="inline-flex items-center rounded bg-emerald-50 px-2.5 py-1 text-xs font-semibold text-emerald-700 border border-emerald-200">
                      Executando
                    </span>
                  </div>
                </div>
                <div className="flex items-center border-l-4 border-gray-200 pl-4 py-1">
                  <div className="space-y-1">
                    <p className="text-[15px] font-bold text-[#1a202c]">Tailor Agent (Currículo)</p>
                    <p className="text-sm text-[#4a5568]">Aguardando nova oportunidade de match.</p>
                  </div>
                  <div className="ml-auto">
                    <span className="inline-flex items-center rounded bg-gray-100 px-2.5 py-1 text-xs font-semibold text-gray-600 border border-gray-200">
                      Ocioso
                    </span>
                  </div>
                </div>
                <div className="flex items-center border-l-4 border-blue-500 pl-4 py-1">
                  <div className="space-y-1">
                    <p className="text-[15px] font-bold text-[#1a202c]">Interview Agent (Mock)</p>
                    <p className="text-sm text-[#4a5568]">Agendado para simular entrevista amanhã.</p>
                  </div>
                  <div className="ml-auto">
                    <span className="inline-flex items-center rounded bg-blue-50 px-2.5 py-1 text-xs font-semibold text-blue-700 border border-blue-200">
                      Agendado
                    </span>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card className="col-span-3 shadow-sm border-gray-200">
              <CardHeader>
                <CardTitle className="text-[#1a202c]">Matches Recentes</CardTitle>
                <CardDescription>Oportunidades com maior aderência (RAG).</CardDescription>
              </CardHeader>
              <CardContent className="space-y-5">
                 <div className="flex flex-col space-y-1 p-3 rounded-lg bg-[#f0f4f8]/50 border border-transparent hover:border-gray-200 transition-colors cursor-pointer">
                    <span className="text-[15px] font-bold text-[#1a202c]">Cloud Engineer Sênior</span>
                    <span className="text-sm text-[#4a5568]">VitaCore Health • Remoto</span>
                    <span className="text-sm font-black text-emerald-600 mt-1">92% Match</span>
                 </div>
                 <div className="flex flex-col space-y-1 p-3 rounded-lg bg-[#f0f4f8]/50 border border-transparent hover:border-gray-200 transition-colors cursor-pointer">
                    <span className="text-[15px] font-bold text-[#1a202c]">Especialista DevOps (AWS)</span>
                    <span className="text-sm text-[#4a5568]">Empresa Confidencial • São Paulo</span>
                    <span className="text-sm font-black text-emerald-600 mt-1">88% Match</span>
                 </div>
              </CardContent>
            </Card>
          </div>

        </div>
      </main>
    </div>
  )
}
