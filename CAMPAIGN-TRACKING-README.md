# 🎯 Campaign Tracking Structure - Wolf Carpenters

## 📋 Visão Geral

Estrutura completa de rastreamento de campanhas publicitárias implementada com sucesso! Esta configuração permite identificar de qual plataforma (Google Ads, Meta Ads, etc.) cada visitante veio.

## 🗂️ Estrutura de Arquivos Criada

```
KITCHEN REMODELING/
├── index.html                      # Menu Hub (página de seleção de campanha)
├── index-original-backup.html      # Backup da landing page original
├── google/
│   └── index.html                  # Landing page com tracking do Google
└── meta/
    └── index.html                  # Landing page com tracking do Meta
```

## 🌐 URLs de Acesso

### Menu Hub (não indexado)
- URL: `https://seudominio.com/`
- Função: Página de navegação com botões para cada campanha
- Meta tag: `noindex, nofollow` (não aparece no Google)

### Landing Pages com Clean URLs
- **Google Ads**: `https://seudominio.com/google/`
- **Meta Ads**: `https://seudominio.com/meta/`

**Nota**: As URLs funcionam SEM a extensão .html graças à estrutura de pastas com index.html

## 🎨 Design do Menu Hub

### Características:
- ✅ Design minimalista e profissional
- ✅ Logo centralizado da Wolf Carpenters
- ✅ Título explicativo
- ✅ Botões estilizados com cores das plataformas:
  - **Google**: Gradiente colorido (azul, verde, amarelo, vermelho)
  - **Meta**: Azul característico do Facebook (#0866FF)
- ✅ Efeitos hover suaves
- ✅ Totalmente responsivo (mobile, tablet, desktop)

## 📊 Sistema de Tracking

### Como Funciona:

Cada landing page tem um script no início do `<head>` que salva a origem no `sessionStorage`:

**Google (`/google/index.html`):**
```javascript
sessionStorage.setItem('campanha_fonte', 'google');
sessionStorage.setItem('campanha_plataforma', 'GOOGLE');
```

**Meta (`/meta/index.html`):**
```javascript
sessionStorage.setItem('campanha_fonte', 'meta');
sessionStorage.setItem('campanha_plataforma', 'META');
```

### Como Usar os Dados:

No formulário de contato, você pode capturar a origem assim:

```javascript
// Exemplo de captura no formulário
const fonte = sessionStorage.getItem('campanha_fonte') || 'direto';
const plataforma = sessionStorage.getItem('campanha_plataforma') || 'DIRETO';

// Adicionar ao envio do formulário
formData.append('origem', fonte);
formData.append('plataforma', plataforma);
```

## ✨ Benefícios da Estrutura

1. **URLs Profissionais**: Sem extensão .html nas URLs
2. **Rastreamento Preciso**: Identifica origem de cada lead
3. **Fácil Expansão**: Para adicionar TikTok, basta:
   ```bash
   mkdir tiktok
   cp index-original-backup.html tiktok/index.html
   # Editar o tracking para 'tiktok' e 'TIKTOK'
   ```
4. **Compatível com GitHub Pages**: Funciona sem configuração de servidor
5. **SEO Controlado**: Menu hub não é indexado
6. **Conteúdo Idêntico**: Todas as landing pages têm o mesmo conteúdo

## 🔧 Como Adicionar Nova Plataforma

**Exemplo: Adicionar TikTok**

1. Criar pasta e copiar conteúdo:
```bash
mkdir tiktok
cp index-original-backup.html tiktok/index.html
```

2. Editar o tracking em `tiktok/index.html`:
```javascript
sessionStorage.setItem('campanha_fonte', 'tiktok');
sessionStorage.setItem('campanha_plataforma', 'TIKTOK');
```

3. Adicionar botão no menu hub (`index.html`):
```html
<a href="/tiktok/" class="campaign-button tiktok-button">
    <span class="button-icon">🎵</span>
    <span>TikTok Ads Campaign</span>
</a>
```

4. Adicionar estilo para o botão no CSS:
```css
.tiktok-button {
    background: #000000;
    color: white;
}
```

## 📱 Responsividade

O menu hub é totalmente responsivo:
- **Desktop**: Layout amplo e espaçado
- **Tablet**: Ajustes de padding e fontes
- **Mobile**: Layout otimizado para telas pequenas

## 🔐 Segurança

✅ **Scan Snyk Code executado**: 0 vulnerabilidades encontradas
✅ **Código limpo e seguro**

## 🚀 Deploy no GitHub Pages

Esta estrutura funciona perfeitamente no GitHub Pages sem configuração adicional:

1. Faça push dos arquivos para o repositório
2. Ative GitHub Pages nas configurações
3. As URLs limpas funcionarão automaticamente

## 📞 Suporte

Para dúvidas ou suporte, consulte a documentação ou entre em contato com o time de desenvolvimento.

---

**Criado em**: 2 de fevereiro de 2026  
**Versão**: 1.0  
**Status**: ✅ Implementado e testado
