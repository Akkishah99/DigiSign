using System;
using System.IO;
using System.Text;
using iText.Kernel.Pdf;
using iText.Kernel.Font;
using iText.Layout;
using iText.Layout.Element;
using iText.Layout.Properties;

namespace DigiSignPdfGenerator
{
    /// <summary>
    /// PDF Generator using iTextSharp library
    /// Converts base64-encoded XML content to formatted PDF
    /// </summary>
    public class PdfGenerator
    {
        /// <summary>
        /// Generate PDF from XML content (in-memory)
        /// </summary>
        public static byte[] GeneratePdfInMemory(string xmlContent)
        {
            try
            {
                var outputStream = new MemoryStream();

                // Create PDF writer and document
                PdfWriter writer = new PdfWriter(outputStream);
                PdfDocument pdfDocument = new PdfDocument(writer);
                Document document = new Document(pdfDocument);

                // Set document margins
                document.SetMargins(20, 20, 20, 20);

                // Add title
                Paragraph title = new Paragraph("Digital Signature Report")
                    .SetFont(PdfFontFactory.CreateFont(iText.IO.Font.Constants.StandardFonts.HELVETICA_BOLD))
                    .SetFontSize(18)
                    .SetTextAlignment(TextAlignment.CENTER);
                document.Add(title);

                // Add spacing
                document.Add(new Paragraph("\n"));

                // Format and add XML content line by line
                string formattedXml = xmlContent.Replace("><", ">\n<");
                string[] lines = formattedXml.Split(new[] { "\n" }, StringSplitOptions.None);

                PdfFont regularFont = PdfFontFactory.CreateFont(iText.IO.Font.Constants.StandardFonts.COURIER);
                foreach (string line in lines)
                {
                    if (!string.IsNullOrWhiteSpace(line))
                    {
                        Paragraph xmlLine = new Paragraph(line)
                            .SetFont(regularFont)
                            .SetFontSize(9);
                        document.Add(xmlLine);
                    }
                }

                // Add footer
                document.Add(new Paragraph("\n"));
                Paragraph footer = new Paragraph("This PDF was auto-generated from a digitally signed XML payload.")
                    .SetFont(PdfFontFactory.CreateFont(iText.IO.Font.Constants.StandardFonts.HELVETICA_OBLIQUE))
                    .SetFontSize(8)
                    .SetTextAlignment(TextAlignment.CENTER);
                document.Add(footer);

                // Close document
                document.Close();

                // Return PDF bytes
                return outputStream.ToArray();
            }
            catch (Exception ex)
            {
                throw new InvalidOperationException($"PDF generation failed: {ex.Message}", ex);
            }
        }
    }
}
