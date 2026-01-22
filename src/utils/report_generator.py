
import os
import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import mm
import matplotlib.pyplot as plt

def generate_pdf_report(save_path, data, logo_path=None):
    """
    Generate a professional PDF report for the BMS data.
    """
    
    # Create plot image (smaller height)
    plot_img_path = save_path.replace('.pdf', '_plot.png')
    have_plot = _create_plot_image(data.get('Cells', []), plot_img_path)
    
    try:
        # Tighter margins for single page
        doc = SimpleDocTemplate(save_path, pagesize=A4,
                                rightMargin=10*mm, leftMargin=10*mm,
                                topMargin=10*mm, bottomMargin=10*mm)

        styles = getSampleStyleSheet()
        
        # Compact Styles
        style_title = ParagraphStyle(
            'ReportTitle', 
            parent=styles['Heading1'],
            fontSize=20,  # Reduced from 24
            leading=24,
            textColor=colors.HexColor('#003045'),
            alignment=1, # Center
            spaceAfter=5  # Reduced from 10
        )
        
        style_subtitle = ParagraphStyle(
            'ReportSubtitle',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#666666'),
            alignment=1,
            spaceAfter=10 # Reduced from 20
        )
        
        style_section = ParagraphStyle(
            'SectionHeader',
            parent=styles['Heading2'],
            fontSize=12, # Reduced from 14
            textColor=colors.HexColor('#007acc'),
            spaceBefore=8, # Reduced from 15
            spaceAfter=5,  # Reduced from 10
            borderPadding=2,
            borderWidth=0,
            borderColor=colors.HexColor('#007acc'),
            backColor=None 
        )
        
        style_stats = ParagraphStyle(
            'Stats', 
            parent=styles['Normal'], 
            fontSize=9, 
            alignment=1
        )

        elements = []
        
        # --- Header Section (Compact) ---
        header_data = []
        if logo_path and os.path.exists(logo_path):
            img = Image(logo_path, width=35*mm, height=35*mm, kind='proportional')
            header_data.append([img, Paragraph("<b>BATTERY DIAGNOSTIC REPORT</b>", style_title)])
        else:
            header_data.append([Paragraph("<b>BATTERY DIAGNOSTIC REPORT</b>", style_title)])
            
        if len(header_data[0]) == 2:
            t = Table(header_data, colWidths=[40*mm, 120*mm])
            t.setStyle(TableStyle([
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ]))
            elements.append(t)
        else:
            elements.append(Paragraph("BATTERY DIAGNOSTIC REPORT", style_title))

        elements.append(Paragraph(f"Generated: {datetime.datetime.now().strftime('%d %B %Y - %H:%M:%S')}", style_subtitle))
        elements.append(Spacer(1, 2*mm))
        
        # --- PASS/FAIL Summary ---
        safety_status = str(data.get('SafetyStatusStr', 'Unknown'))
        pf_status = str(data.get('PFStatusStr', 'Unknown'))
        
        overall_status = "PASS"
        status_color = colors.green
        if "OK" not in safety_status or "No Permanent Failure" not in pf_status:
            overall_status = "FAIL / ATTENTION"
            status_color = colors.red

        status_text = f"<b>OVERALL STATUS: <font color={status_color}>{overall_status}</font></b>"
        elements.append(Paragraph(status_text, ParagraphStyle('Status', parent=styles['Normal'], fontSize=11, alignment=1, spaceAfter=8)))
        
        # --- Section 1: Device Overview ---
        elements.append(Paragraph("Device Overview", style_section))
        
        param_data = [
            ['Parameter', 'Value', 'Parameter', 'Value'],
            ['Pack Voltage', f"{data.get('PackVoltage_mV', '---')} mV", 'Gauge Type', str(data.get('GaugeType', '---'))],
            ['Current', f"{data.get('Current_mA', '---')} mA", 'Cycle Count', str(data.get('CycleCount', '---'))],
            ['Temperature', f"{data.get('Temperature_C', '---')} °C", 'Chemistry', 'LION'],
            ['Rem. Capacity', f"{data.get('RemainCapacity_mAh', '---')} mAh", 'Full Capacity', f"{data.get('FullCapacity_mAh', '---')} mAh"],
        ]
        
        # Slightly wider columns for single page width usage
        t_params = Table(param_data, colWidths=[45*mm, 50*mm, 45*mm, 50*mm])
        t_params.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#007acc')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 9), # Slightly smaller font
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
            ('BACKGROUND', (0,1), (-1,-1), colors.whitesmoke),
        ]))
        elements.append(t_params)
        elements.append(Spacer(1, 5*mm))
        
        # --- Section 2: Safety Diagnostics ---
        elements.append(Paragraph("Safety Diagnostics", style_section))
        
        safety_data = [
            ['Diagnostic Check', 'Status'],
            ['Safety Alerts', safety_status],
            ['Permanent Failures', pf_status],
        ]
        
        t_safety = Table(safety_data, colWidths=[60*mm, 130*mm])
        t_safety.setStyle(TableStyle([
             ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#007acc')),
             ('TEXTCOLOR', (0,0), (-1,0), colors.white),
             ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
             ('FONTSIZE', (0,0), (-1,-1), 9),
             ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
             ('PADDING', (0,0), (-1,-1), 6),
             ('BACKGROUND', (0,1), (-1,-1), colors.whitesmoke),
        ]))
        elements.append(t_safety)
        elements.append(Spacer(1, 5*mm))
        
        # --- Section 3: Cell Analysis ---
        if have_plot:
            elements.append(Paragraph("Cell Voltage Analysis", style_section))
            # Reduce image height to fit
            im = Image(plot_img_path, width=170*mm, height=55*mm)
            elements.append(im)
            
            # Simple stats
            cells = data.get('Cells', [])
            if cells:
                 min_v = min(cells)
                 max_v = max(cells)
                 delta = max_v - min_v
                 avg_v = sum(cells)/len(cells)
                 
                 stats_text = f"<b>Statistics:</b> Min: {min_v}mV | Max: {max_v}mV | Delta: {delta}mV | Avg: {int(avg_v)}mV"
                 elements.append(Spacer(1, 2*mm))
                 elements.append(Paragraph(stats_text, style_stats))

        # Footer (Minimal)
        elements.append(Spacer(1, 8*mm))
        elements.append(Paragraph("<i>End of Report - Generated by Amplyze</i>", style_subtitle))

        doc.build(elements)
        
        # Cleanup
        if os.path.exists(plot_img_path):
            try:
                os.remove(plot_img_path)
            except:
                pass
                
        return True
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return False

def _create_plot_image(cells, save_path):
    try:
        if not cells: return False
        
        fig, ax = plt.subplots(figsize=(8, 3), dpi=150)
        
        x = list(range(1, len(cells) + 1))
        
        # Modern Plot Style
        ax.bar(x, cells, color='#007acc', alpha=0.7, width=0.6, label='Voltage')
        ax.plot(x, cells, color='#003045', marker='o', linewidth=2, label='Trend')
        
        # Limits based on typical Li-ion
        avg = sum(cells)/len(cells)
        ax.set_ylim(min(cells)-50, max(cells)+50)
        
        ax.axhline(y=avg, color='#ff6b6b', linestyle='--', alpha=0.8, label=f'Avg: {int(avg)}')
        
        ax.set_title('Cell Voltage Distribution', fontsize=12, fontweight='bold', color='#333')
        ax.set_ylabel('Voltage (mV)')
        ax.set_xlabel('Cell Serial Number')
        ax.set_xticks(x)
        ax.grid(axis='y', linestyle='--', alpha=0.5)
        ax.legend()
        
        # Despine
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        plt.tight_layout()
        fig.savefig(save_path, bbox_inches='tight')
        plt.close(fig)
        return True
    except Exception as e:
        print(f"Error plotting: {e}")
        return False
