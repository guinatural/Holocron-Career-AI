import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'

export default function Home() {
  return (
    <div className="flex-1 space-y-4 p-8 pt-6 max-w-7xl mx-auto w-full">
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">Dashboard</h2>
        <div className="flex items-center space-x-2">
          <Button>Analisar Currículo</Button>
        </div>
      </div>
      
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Vagas Analisadas
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">14</div>
            <p className="text-xs text-muted-foreground">
              +2 desde ontem
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Aplicações Ativas
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">6</div>
            <p className="text-xs text-muted-foreground">
              3 em fase de entrevista
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Interações com Agentes
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">89</div>
            <p className="text-xs text-muted-foreground">
              +12% vs mês passado
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Score Médio (ATS)
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">84%</div>
            <p className="text-xs text-muted-foreground">
              Alta probabilidade de match
            </p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
        <Card className="col-span-4">
          <CardHeader>
            <CardTitle>Meus Agentes</CardTitle>
            <CardDescription>
              Seus agentes especializados trabalhando por você.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center">
              <div className="ml-4 space-y-1">
                <p className="text-sm font-medium leading-none">Scout Agent (Pesquisa)</p>
                <p className="text-sm text-muted-foreground">
                  Procurando vagas em Next.js e AWS na Gupy e LinkedIn
                </p>
              </div>
              <div className="ml-auto font-medium">
                <span className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-400">
                  Rodando
                </span>
              </div>
            </div>
            <div className="flex items-center">
              <div className="ml-4 space-y-1">
                <p className="text-sm font-medium leading-none">Tailor Agent (Currículo)</p>
                <p className="text-sm text-muted-foreground">
                  Aguardando nova vaga alvo
                </p>
              </div>
              <div className="ml-auto font-medium">
                <span className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold text-muted-foreground">
                  Ocioso
                </span>
              </div>
            </div>
            <div className="flex items-center">
              <div className="ml-4 space-y-1">
                <p className="text-sm font-medium leading-none">Mock Agent (Entrevista)</p>
                <p className="text-sm text-muted-foreground">
                  Agendado para hoje às 19:00
                </p>
              </div>
              <div className="ml-auto font-medium">
                <span className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400">
                  Agendado
                </span>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card className="col-span-3">
          <CardHeader>
            <CardTitle>Vagas Recentes (Match)</CardTitle>
            <CardDescription>
              Encontradas pelo Scout Agent.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
             <div className="space-y-1">
                <p className="text-sm font-medium leading-none">Cloud Engineer Sênior</p>
                <p className="text-xs text-muted-foreground">VitaCore Health • Remoto</p>
                <p className="text-xs font-bold text-emerald-500">92% Match</p>
             </div>
             <div className="space-y-1">
                <p className="text-sm font-medium leading-none">Especialista DevOps (AWS)</p>
                <p className="text-xs text-muted-foreground">Nubank • São Paulo</p>
                <p className="text-xs font-bold text-emerald-500">88% Match</p>
             </div>
             <div className="space-y-1">
                <p className="text-sm font-medium leading-none">SRE Pleno</p>
                <p className="text-xs text-muted-foreground">Mercado Livre • Remoto</p>
                <p className="text-xs font-bold text-emerald-500">81% Match</p>
             </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
