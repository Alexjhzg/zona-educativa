import { ref } from 'vue'
import QRCode from 'qrcode'
import { toast } from 'vue3-toastify'

export function useQrReport() {
  const generandoReporte = ref(false)

  // Generar reporte PNG de un solo QR (Canvas 2D puro)
  const generarReporteQR = async (qrItem, currentPlantel) => {
    const plantel = typeof currentPlantel === 'function' ? currentPlantel() : currentPlantel.value
    if (!qrItem || !plantel) return
    generandoReporte.value = true

    try {
      const qrSize = 260
      const pad = 48

      // Generar QR como DataURL
      const qrDataUrl = await QRCode.toDataURL(qrItem.value, {
        width: qrSize,
        margin: 1,
        color: { dark: '#000000', light: '#ffffff' },
        errorCorrectionLevel: 'H'
      })

      // Dimensiones del canvas
      const totalW = qrSize + pad * 2
      const headerH = 80   // nombre plantel + línea
      const labelH  = 40   // etiqueta QR
      const footerH = 40
      const totalH  = headerH + qrSize + labelH + footerH + pad

      const canvas = document.createElement('canvas')
      canvas.width  = totalW
      canvas.height = totalH
      const ctx = canvas.getContext('2d')

      // Fondo blanco
      ctx.fillStyle = '#ffffff'
      ctx.fillRect(0, 0, totalW, totalH)

      // --- NOMBRE DEL PLANTEL (header) ---
      ctx.fillStyle = '#0f172a'
      ctx.font = 'bold 16px Inter, Arial, sans-serif'
      ctx.textAlign = 'center'
      ctx.textBaseline = 'middle'
      // Wrap: truncar si excede el ancho
      let nombre = plantel.plantel || 'Plantel Educativo'
      const maxW = totalW - 24
      while (ctx.measureText(nombre).width > maxW && nombre.length > 10) {
        nombre = nombre.slice(0, -1)
      }
      ctx.fillText(nombre, totalW / 2, 32)

      // Línea separadora
      ctx.strokeStyle = '#e2e8f0'
      ctx.lineWidth = 1
      ctx.beginPath()
      ctx.moveTo(pad / 2, 56)
      ctx.lineTo(totalW - pad / 2, 56)
      ctx.stroke()

      // --- ETIQUETA DEL QR ---
      ctx.fillStyle = '#64748b'
      ctx.font = 'bold 11px Inter, Arial, sans-serif'
      ctx.textAlign = 'center'
      ctx.textBaseline = 'middle'
      ctx.fillText(qrItem.label, totalW / 2, headerH - 8)

      // --- IMAGEN QR ---
      const img = new Image()
      img.src = qrDataUrl
      await new Promise(res => { img.onload = res })
      ctx.drawImage(img, pad, headerH, qrSize, qrSize)

      // --- FOOTER ---
      ctx.fillStyle = '#94a3b8'
      ctx.font = '10px Inter, Arial, sans-serif'
      ctx.textAlign = 'center'
      ctx.textBaseline = 'middle'
      const fecha = new Date().toLocaleDateString('es-VE', { day: '2-digit', month: 'long', year: 'numeric' })
      ctx.fillText(`Zona Educativa Monagas · ${fecha}`, totalW / 2, headerH + qrSize + labelH + footerH / 2 - 4)

      // Descargar
      const link = document.createElement('a')
      const slug = (plantel.plantel || 'qr')
        .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
        .replace(/[^a-zA-Z0-9 -]/g, '').replace(/\s+/g, '_').toLowerCase().slice(0, 50)
      link.download = `QR_${qrItem.key}_${slug}.png`
      link.href = canvas.toDataURL('image/png')
      link.click()
      toast.success(`Reporte ${qrItem.label} descargado`)
    } catch (err) {
      console.error('Error generando reporte QR:', err)
      toast.error('Error al generar el reporte')
    } finally {
      generandoReporte.value = false
    }
  }

  return {
    generandoReporte,
    generarReporteQR
  }
}
