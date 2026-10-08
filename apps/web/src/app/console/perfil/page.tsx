'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'

export default function PerfilPage() {
  const [file, setFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)
  const [message, setMessage] = useState('')

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0])
    }
  }

  const handleUpload = async () => {
    if (!file) return
    setUploading(true)
    setMessage('')

    const formData = new FormData()
    formData.append("file", file)

    try {
      // Fazendo a chamada real para a nossa FastAPI que extrai texto via PyPDF2 
      // e injeta no ChromaDB via Amazon Bedrock (RAG)
      const res = await fetch("http://localhost:8000/api/v1/upload-resume/guilherme-123", {
        method: "POST",
        body: formData,
      })
      
      const data = await res.json()
      
      if (!res.ok) {
        throw new Error(data.detail || "Falha no upload")
      }
      
      setMessage("✅ Currículo processado com sucesso! " + data.extracted_length + " caracteres vetorizados.")
    } catch (err: any) {
      setMessage("❌ Erro: " + err.message)
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="p-8 max-w-4xl space-y-8">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-[#1a202c]">Meu Perfil</h1>
        <p className="text-[#4a5568]">Alimente o banco de dados vetorial da IA com o seu currículo.</p>
      </div>

      <Card className="shadow-sm border-gray-200">
        <CardHeader>
          <CardTitle>Base de Conhecimento (RAG)</CardTitle>
          <CardDescription>
            Faça o upload do seu currículo em formato PDF. Nosso pipeline extrai o texto, converte em vetores (Embeddings) na AWS e o armazena pronto para o Tailor Agent analisar as vagas.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="flex flex-col sm:flex-row items-start sm:items-center gap-4">
            <Input 
              type="file" 
              accept="application/pdf" 
              onChange={handleFileChange}
              className="max-w-md cursor-pointer file:text-sm file:font-semibold"
            />
            <Button 
              onClick={handleUpload} 
              disabled={!file || uploading}
              className="bg-[#232F3E] hover:bg-[#1a232e] text-white"
            >
              {uploading ? "Processando e Vetorizando..." : "Enviar PDF"}
            </Button>
          </div>
          
          {message && (
            <div className={`p-4 rounded-md text-sm font-medium ${message.includes('Erro') ? 'bg-red-50 text-red-700 border border-red-200' : 'bg-emerald-50 text-emerald-700 border border-emerald-200'}`}>
              {message}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
