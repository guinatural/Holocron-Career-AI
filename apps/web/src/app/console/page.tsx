import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

export default function ConsoleDashboard() {
  return (
    <div className="p-8 space-y-8">
      <div className="mb-4">
        <h1 className="text-2xl font-bold text-[#1a202c]">Visão Geral</h1>
      </div>
      
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
        {/* Adicionei os outros cards abaixo simplificados */}
        <Card className="shadow-sm border-gray-200">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-semibold text-[#4a5568]">Score Médio (ATS)</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-black text-[#FF9900]">84%</div>
            <p className="text-xs text-[#4a5568] font-medium mt-1">Alta probabilidade de match</p>
          </CardContent>
        </Card>
      </div>

      <Card className="shadow-sm border-gray-200">
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
        </CardContent>
      </Card>
    </div>
  )
}
