from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


class PresupuestoPdfReport:

    def __init__(self, presupuesto, capitulos, items):
        self.presupuesto = presupuesto
        self.capitulos = capitulos
        self.items = items
        self.styles = getSampleStyleSheet()

    def money(self, value):
        try:
            return f"${float(value or 0):,.2f}"
        except Exception:
            return "$0.00"

    def generate(self, filename):
        doc = SimpleDocTemplate(
            filename,
            pagesize=letter,
            rightMargin=35,
            leftMargin=35,
            topMargin=35,
            bottomMargin=35
        )

        content = []

        content.append(Paragraph("PRESUPUESTO BUILDORA", self.styles["Title"]))
        content.append(Spacer(1, 12))

        content.append(self.build_summary_table())
        content.append(Spacer(1, 16))

        content.append(Paragraph("Capítulos del Presupuesto", self.styles["Heading2"]))
        content.append(self.build_chapters_table())
        content.append(Spacer(1, 16))

        content.append(Paragraph("Ítems del Presupuesto", self.styles["Heading2"]))
        content.append(self.build_items_table())

        doc.build(content)

        return filename

    def build_summary_table(self):
        data = [
            ["Código", self.presupuesto.get("codigo_presupuesto", "")],
            ["Nombre", self.presupuesto.get("nombre_presupuesto", "")],
            ["Proyecto", self.presupuesto.get("nombre_proyecto", "")],
            ["Cliente", self.presupuesto.get("nombre_cliente", "")],
            ["Fecha", str(self.presupuesto.get("fecha_presupuesto", ""))],
            ["Costo directo", self.money(self.presupuesto.get("costo_directo_total"))],
            ["Administración", self.money(self.presupuesto.get("total_administracion"))],
            ["Imprevistos", self.money(self.presupuesto.get("total_imprevistos"))],
            ["Utilidad", self.money(self.presupuesto.get("total_utilidad"))],
            ["IVA utilidad", self.money(self.presupuesto.get("iva_utilidad"))],
            ["VALOR TOTAL", self.money(self.presupuesto.get("valor_total_presupuesto"))],
        ]

        table = Table(data, colWidths=[140, 360])

        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#1F4E78")),
            ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
            ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#D9EAF7")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("PADDING", (0, 0), (-1, -1), 6),
        ]))

        return table

    def build_chapters_table(self):
        data = [["Código", "Capítulo", "Costo", "%"]]

        for chapter in self.capitulos:
            data.append([
                chapter.get("codigo_capitulo", ""),
                chapter.get("nombre_capitulo", ""),
                self.money(chapter.get("costo_total_capitulo")),
                f"{float(chapter.get('porcentaje_participacion') or 0):,.2f}%"
            ])

        table = Table(data, colWidths=[80, 250, 110, 60])

        table.setStyle(self.default_table_style())

        return table

    def build_items_table(self):
        data = [["Capítulo", "Ítem", "Descripción", "Und", "Cant.", "Vr Unit.", "Vr Total"]]

        for item in self.items:
            data.append([
                item.get("nombre_capitulo", ""),
                item.get("codigo_item", ""),
                item.get("descripcion_item", ""),
                item.get("unidad_item", ""),
                str(item.get("cantidad", "")),
                self.money(item.get("costo_unitario_historico")),
                self.money(item.get("costo_total_item")),
            ])

        table = Table(
            data,
            colWidths=[80, 55, 165, 40, 50, 80, 80],
            repeatRows=1
        )

        table.setStyle(self.default_table_style())

        return table

    def default_table_style(self):
        return TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E78")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("PADDING", (0, 0), (-1, -1), 4),
        ])