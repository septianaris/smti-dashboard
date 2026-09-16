import os
import subprocess
import time

html_path = os.path.abspath(r"d:\Kerjaan\Laporan_Kegiatan_SMTI.html")
pdf_path = os.path.abspath(r"d:\Kerjaan\Laporan_Kegiatan_SMTI_Terbaru.pdf")

html_content = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Laporan Rincian Kegiatan - Dept. SMTI PT Pupuk Kujang</title>
<style>
  @page {
    size: A4 portrait;
    margin: 12mm 15mm 10mm 15mm;
  }
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    font-family: 'Segoe UI', Arial, Helvetica, sans-serif;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }
  body {
    background-color: #ffffff;
    color: #1e293b;
    font-size: 9.5pt;
    line-height: 1.4;
  }

  /* Document Title Card (Tanpa Header Kop Surat) */
  .title-card {
    background: linear-gradient(to right, #f8fafc, #f1f5f9);
    border-left: 5px solid #003b73;
    border-top: 1px solid #e2e8f0;
    border-right: 1px solid #e2e8f0;
    border-bottom: 1px solid #e2e8f0;
    padding: 10px 14px;
    border-radius: 5px;
    margin-bottom: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .title-card h1 {
    font-size: 13pt;
    color: #003b73;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  .title-card .sub-title {
    font-size: 8.5pt;
    color: #475569;
    margin-top: 2px;
    font-weight: 500;
  }
  .title-badge {
    background: #003b73;
    color: #ffffff;
    font-size: 7.5pt;
    padding: 4px 10px;
    border-radius: 4px;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
  }

  /* Metadata Strip */
  .meta-strip {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 5px;
    padding: 8px 12px;
    margin-bottom: 12px;
    font-size: 8pt;
  }
  .meta-col .label {
    color: #64748b;
    font-weight: 600;
    font-size: 7pt;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  .meta-col .val {
    color: #0f172a;
    font-weight: 700;
    margin-top: 1px;
  }

  /* Highlights / Status Cards */
  .highlights {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-bottom: 14px;
  }
  .h-card {
    border: 1px solid #e2e8f0;
    border-radius: 5px;
    padding: 8px 12px;
    background: #ffffff;
  }
  .h-card.amber { border-top: 3px solid #f59e0b; background: #fffbeb; }
  .h-card.purple { border-top: 3px solid #8b5cf6; background: #faf5ff; }
  .h-title {
    font-size: 7pt;
    color: #475569;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.3px;
  }
  .h-status {
    font-size: 10pt;
    font-weight: 800;
    margin: 2px 0;
  }
  .h-card.amber .h-status { color: #b45309; }
  .h-card.purple .h-status { color: #6d28d9; }
  .h-desc {
    font-size: 7.5pt;
    color: #64748b;
    line-height: 1.35;
  }

  /* Section Title */
  .section-title {
    font-size: 9.5pt;
    font-weight: 700;
    color: #003b73;
    border-left: 3.5px solid #008751;
    padding-left: 8px;
    margin: 12px 0 8px 0;
    text-transform: uppercase;
    letter-spacing: 0.3px;
  }

  /* Table */
  table.matrix-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 18px;
    font-size: 8.5pt;
  }
  table.matrix-table th {
    background-color: #003b73;
    color: #ffffff;
    padding: 8px 10px;
    font-weight: 700;
    font-size: 8pt;
    border: 1px solid #003b73;
    text-transform: uppercase;
    letter-spacing: 0.3px;
  }
  table.matrix-table td {
    padding: 10px 12px;
    border: 1px solid #cbd5e1;
    vertical-align: middle;
    line-height: 1.45;
  }
  table.matrix-table tr:nth-child(even) td {
    background-color: #f8fafc;
  }

  /* Status Badges */
  .badge {
    display: inline-block;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 7pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.3px;
    white-space: nowrap;
  }
  .badge-waiting {
    background: #fef3c7;
    color: #92400e;
    border: 1px solid #fcd34d;
  }
  .badge-pending {
    background: #f3e8ff;
    color: #6b21a8;
    border: 1px solid #d8b4fe;
  }

  /* Signatures */
  .signatures {
    display: flex;
    justify-content: space-between;
    margin-top: 18px;
    padding-top: 6px;
    page-break-inside: avoid;
  }
  .sig-block {
    text-align: center;
    width: 30%;
  }
  .sig-block .sig-role {
    font-size: 8pt;
    color: #475569;
    font-weight: 600;
    margin-bottom: 48px;
  }
  .sig-block .sig-name {
    font-size: 8.5pt;
    font-weight: 700;
    color: #0f172a;
    text-decoration: underline;
  }
  .sig-block .sig-sub {
    font-size: 7.5pt;
    color: #64748b;
    margin-top: 2px;
  }

  /* Footer */
  .footer {
    border-top: 1px dashed #cbd5e1;
    margin-top: 16px;
    padding-top: 6px;
    display: flex;
    justify-content: space-between;
    font-size: 7pt;
    color: #94a3b8;
  }
</style>
</head>
<body>

  <!-- TITLE CARD (TANPA HEADER KOP SURAT) -->
  <div class="title-card">
    <div>
      <h1>Laporan Rincian Kegiatan Pekerjaan</h1>
      <div class="sub-title">Departemen Sistem Manajemen Terintegrasi (SMTI) | PT Pupuk Kujang</div>
    </div>
    <div>
      <span class="title-badge">Status Terkini</span>
    </div>
  </div>

  <!-- METADATA STRIP -->
  <div class="meta-strip">
    <div class="meta-col">
      <div class="label">Departemen</div>
      <div class="val">SMTI</div>
    </div>
    <div class="meta-col">
      <div class="label">Perusahaan</div>
      <div class="val">PT Pupuk Kujang</div>
    </div>
    <div class="meta-col">
      <div class="label">Tanggal Pelaporan</div>
      <div class="val">September 2026</div>
    </div>
    <div class="meta-col">
      <div class="label">Klasifikasi</div>
      <div class="val">Laporan Internal</div>
    </div>
  </div>

  <!-- HIGHLIGHTS CARDS -->
  <div class="highlights">
    <div class="h-card amber">
      <div class="h-title">1. Pendampingan SNI</div>
      <div class="h-status">MENUNGGU KE PENGADAAN</div>
      <div class="h-desc">SR telah difollow-up, saat ini menunggu dikirim ke Dept. Pengadaan.</div>
    </div>
    <div class="h-card amber">
      <div class="h-title">2. Sarpras KIX 2026</div>
      <div class="h-status">MENUNGGU PENGADAAN</div>
      <div class="h-desc">Dari Dept. Anggaran menunggu dikirim ke Dept. Pengadaan.</div>
    </div>
    <div class="h-card purple">
      <div class="h-title">3. Kebijakan SMTI</div>
      <div class="h-status">BELUM DITANDATANGANI</div>
      <div class="h-desc">Pengecekan draft selesai, masih belum ditandatangani Direktur Keuangan.</div>
    </div>
  </div>

  <!-- TABEL RINCIAN KEGIATAN -->
  <div class="section-title">Rincian Kegiatan &amp; Status Tindak Lanjut (Follow-Up)</div>

  <table class="matrix-table">
    <thead>
      <tr>
        <th style="width: 5%; text-align: center;">No</th>
        <th style="width: 38%;">Kegiatan / Program</th>
        <th style="width: 37%;">Uraian Tindak Lanjut (Follow-Up)</th>
        <th style="width: 20%; text-align: center;">Status Terkini</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="text-align: center; font-weight: 700;">1</td>
        <td>
          <strong>SR Jasa Pendampingan Sertifikasi SNI Pada Mitra Binaan (Makanan Ringan)</strong>
        </td>
        <td>
          Telah dilakukan proses follow-up terkait pengajuan Service Request (SR) jasa pendampingan sertifikasi SNI untuk mitra binaan makanan ringan, saat ini sedang menunggu dikirim ke Departemen Pengadaan.
        </td>
        <td style="text-align: center;">
          <span class="badge badge-waiting">Menunggu ke Pengadaan</span>
        </td>
      </tr>
      <tr>
        <td style="text-align: center; font-weight: 700;">2</td>
        <td>
          <strong>SR Jasa Penyediaan Sarana &amp; Prasarana Awarding Kujang Innovation Xcellence (KIX) Tahun 2026</strong>
        </td>
        <td>
          Posisi dokumen dari Departemen Anggaran, saat ini sedang menunggu untuk dikirim / diteruskan ke Departemen Pengadaan.
        </td>
        <td style="text-align: center;">
          <span class="badge badge-waiting">Menunggu Dikirim ke Pengadaan</span>
        </td>
      </tr>
      <tr>
        <td style="text-align: center; font-weight: 700;">3</td>
        <td>
          <strong>Pengecekan Dokumen Draft Kebijakan Sistem Manajemen Terintegrasi (SMTI)</strong>
        </td>
        <td>
          Pengecekan dokumen draft kebijakan telah selesai dilakukan, saat ini posisi masih belum ditandatangani oleh Direktur Keuangan PT Pupuk Kujang.
        </td>
        <td style="text-align: center;">
          <span class="badge badge-pending">Belum Ditandatangani Direktur Keuangan</span>
        </td>
      </tr>
    </tbody>
  </table>

  <!-- LEMBAR TANDA TANGAN -->
  <div class="signatures">
    <div class="sig-block">
      <div class="sig-role">Dibuat / Dilaporkan Oleh:</div>
      <div class="sig-name">( ........................................ )</div>
      <div class="sig-sub">PIC / Staf Departemen SMTI</div>
    </div>
    <div class="sig-block">
      <div class="sig-role">Diperiksa Oleh:</div>
      <div class="sig-name">( ........................................ )</div>
      <div class="sig-sub">AVP Sistem Manajemen Terintegrasi</div>
    </div>
    <div class="sig-block">
      <div class="sig-role">Mengetahui / Menyetujui:</div>
      <div class="sig-name">( ........................................ )</div>
      <div class="sig-sub">VP Sistem Manajemen Terintegrasi</div>
    </div>
  </div>

  <!-- FOOTER -->
  <div class="footer">
    <div>PT Pupuk Kujang | Departemen Sistem Manajemen Terintegrasi (SMTI)</div>
    <div>Laporan Kegiatan Pekerjaan | Tanggal: September 2026</div>
  </div>

</body>
</html>
"""

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML saved to: {html_path}")

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
cmd = [
    edge_path,
    "--headless=new",
    "--disable-gpu",
    "--run-all-compositor-stages-before-draw",
    f"--print-to-pdf={pdf_path}",
    "--no-pdf-header-footer",
    html_path
]

print("Converting to PDF...")
result = subprocess.run(cmd, capture_output=True, text=True)
time.sleep(2)

if os.path.exists(pdf_path):
    size = os.path.getsize(pdf_path)
    print(f"SUCCESS: PDF created at {pdf_path} (size: {size} bytes)")
else:
    print(f"FAILED: PDF not found. Error: {result.stderr}")
