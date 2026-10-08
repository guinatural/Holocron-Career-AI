import { Button } from '@/components/ui/button'

export default function Home() {
  return (
    <div className="min-h-screen bg-white font-sans">
      {/* HERO SECTION - Gradient Background */}
      <div className="relative w-full h-[550px] overflow-hidden bg-gradient-to-r from-[#d2d9fc] via-[#e2dcfc] to-[#fce4ea]">
        {/* Background elements to mock the image graphics */}
        <div className="absolute right-0 top-0 w-1/2 h-full opacity-80 overflow-hidden pointer-events-none">
            <div className="absolute top-10 right-10 w-[500px] h-[500px] bg-[#9fd2f6] rounded-full mix-blend-multiply filter blur-sm"></div>
            <div className="absolute top-20 right-20 w-[400px] h-[400px] rounded-full border-[1.5px] border-[#1d4ed8] opacity-20"></div>
            <div className="absolute top-32 right-32 w-[200px] h-[200px] rounded-full border-[1.5px] border-[#1d4ed8] opacity-30"></div>
            {/* Dots mocking the neural network nodes */}
            <div className="absolute top-40 right-40 w-4 h-4 bg-[#1e3a8a] rounded-full"></div>
            <div className="absolute top-60 right-[400px] w-5 h-5 bg-[#1e3a8a] rounded-full"></div>
            <div className="absolute top-80 right-20 w-3 h-3 bg-[#1e3a8a] rounded-full"></div>
            <div className="absolute top-96 right-[300px] w-4 h-4 bg-[#1e3a8a] rounded-full"></div>
            {/* SVG Path simulating the network lines */}
            <svg className="absolute top-0 right-0 w-full h-full" viewBox="0 0 500 500">
                <path d="M 340 160 Q 200 240 100 240 T -20 380" stroke="#1e3a8a" strokeWidth="2" fill="none" opacity="0.4" />
                <path d="M 340 160 Q 400 300 200 380" stroke="#1e3a8a" strokeWidth="2" fill="none" opacity="0.4" />
                <path d="M 100 240 Q 200 400 480 320" stroke="#1e3a8a" strokeWidth="2" fill="none" opacity="0.4" />
            </svg>
        </div>

        <div className="relative z-10 max-w-7xl mx-auto px-6 pt-24 h-full flex">
          {/* Floating Card Content */}
          <div className="bg-[#f2f6fa]/95 backdrop-blur-md max-w-[540px] p-12 rounded-xl shadow-sm border border-white/60 h-fit mt-4">
            <h1 className="text-[2.2rem] leading-[1.2] font-semibold text-[#1a202c] mb-5 tracking-tight">
              Trabalhe com agentes confiáveis para encontrar as vagas certas
            </h1>
            <p className="text-[1.05rem] text-[#4a5568] mb-8 leading-relaxed">
              Aproveite a experiência e as soluções especializadas do ecossistema Holocron para obter melhores resultados em sua carreira com maior rapidez e confiança.
            </p>
            <Button className="bg-[#232F3E] hover:bg-[#1a232e] text-white rounded-full px-8 py-6 text-[15px] font-bold shadow-none">
              Retornar ao console
            </Button>
          </div>
        </div>
      </div>

      {/* MAIN CONTENT AREA - White rounded overlap */}
      <div className="relative z-20 bg-white rounded-tl-[3rem] -mt-16 pt-20 px-6 pb-24">
        <div className="max-w-7xl mx-auto">
          <div className="mb-10">
            <h2 className="text-[1.8rem] font-bold text-[#1a202c] mb-3">Novidades</h2>
            <p className="text-[#4a5568] text-[1.05rem]">
              Acompanhe os lançamentos, atualizações e histórias de sucesso mais comentados em todo o ecossistema Holocron.
            </p>
          </div>

          {/* CARDS SECTION */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Card 1 */}
            <div className="group cursor-pointer rounded-xl overflow-hidden border border-gray-200 hover:shadow-lg transition-all bg-white flex flex-col h-[320px]">
              <div className="h-44 w-full bg-gradient-to-br from-[#101026] via-[#1a103c] to-[#36134d] relative overflow-hidden">
                 <span className="absolute top-4 left-4 bg-white/10 text-white text-xs font-semibold px-2 py-1 rounded backdrop-blur-md">Event</span>
                 {/* Decorative mock blocks */}
                 <div className="absolute bottom-0 left-10 w-16 h-20 border border-indigo-400/30 bg-indigo-500/10"></div>
                 <div className="absolute bottom-10 left-20 w-24 h-24 border border-purple-400/30 bg-purple-500/10"></div>
              </div>
              <div className="p-6 flex-1">
                <h3 className="font-bold text-lg mb-2 text-[#1a202c] group-hover:text-[#FF9900] transition-colors">Novos Agentes de Entrevista</h3>
                <p className="text-[#4a5568] text-sm">Prepare-se para entrevistas técnicas com agentes simulando avaliadores reais.</p>
              </div>
            </div>

            {/* Card 2 */}
            <div className="group cursor-pointer rounded-xl overflow-hidden border border-gray-200 hover:shadow-lg transition-all bg-white flex flex-col h-[320px]">
              <div className="h-44 w-full bg-gradient-to-br from-[#d4c8f5] to-[#f5d0d8] relative overflow-hidden flex items-end justify-center">
                 <span className="absolute top-4 left-4 bg-white/40 text-[#1a202c] text-xs font-semibold px-2 py-1 rounded backdrop-blur-md">AI Agents</span>
                 {/* Decorative mock swirl */}
                 <div className="w-32 h-32 bg-gradient-to-t from-purple-500 to-transparent rounded-t-full opacity-50"></div>
              </div>
              <div className="p-6 flex-1">
                <h3 className="font-bold text-lg mb-2 text-[#1a202c] group-hover:text-[#FF9900] transition-colors">Scout Agent Atualizado</h3>
                <p className="text-[#4a5568] text-sm">Otimização de rastreio de vagas agora suporta mais de 50 portais de emprego no Brasil.</p>
              </div>
            </div>

            {/* Card 3 */}
            <div className="group cursor-pointer rounded-xl overflow-hidden border border-gray-200 hover:shadow-lg transition-all bg-white flex flex-col h-[320px]">
              <div className="h-44 w-full bg-gradient-to-br from-[#fcb086] to-[#e84a7e] relative overflow-hidden">
                 <span className="absolute top-4 left-4 bg-white/20 text-white text-xs font-semibold px-2 py-1 rounded backdrop-blur-md">Data</span>
                 {/* Decorative mock track */}
                 <div className="absolute bottom-0 w-full h-12 bg-white/20 transform -skew-y-6 translate-y-4"></div>
              </div>
              <div className="p-6 flex-1">
                <h3 className="font-bold text-lg mb-2 text-[#1a202c] group-hover:text-[#FF9900] transition-colors">Análise de Dados do Currículo</h3>
                <p className="text-[#4a5568] text-sm">Descubra as palavras-chave que estão faltando no seu perfil com os relatórios automáticos.</p>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  )
}
