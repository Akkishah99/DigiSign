using System;
using System.IO;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;

namespace DigiSignPdfGenerator
{
    public class PdfGeneratorFunction
    {
        /// <summary>
        /// Azure Function: HTTP-triggered PDF generator
        /// Expects POST request with JSON: {"signedText": "<base64-encoded-xml>"}
        /// Returns: PDF file as attachment
        /// </summary>
        [FunctionName("GeneratePdf")]
        public static async Task<IActionResult> Run(
            [HttpTrigger(AuthorizationLevel.Function, "post", Route = null)] HttpRequest req,
            ILogger log)
        {
            log.LogInformation("PDF generation function triggered.");

            try
            {
                // Parse JSON request body
                string requestBody = await new StreamReader(req.Body).ReadToEndAsync();
                dynamic data = JsonConvert.DeserializeObject(requestBody);

                // Extract signedText
                string signedText = data?.signedText;

                if (string.IsNullOrEmpty(signedText))
                {
                    return new BadRequestObjectResult(new { error = "Missing 'signedText' in request body" });
                }

                // Decode Base64
                string xmlContent;
                try
                {
                    byte[] decodedBytes = Convert.FromBase64String(signedText);
                    xmlContent = System.Text.Encoding.UTF8.GetString(decodedBytes);
                }
                catch (FormatException)
                {
                    return new BadRequestObjectResult(new { error = "Invalid Base64 encoding" });
                }
                catch (Exception ex)
                {
                    return new BadRequestObjectResult(new { error = $"Decoding error: {ex.Message}" });
                }

                // Generate PDF using iTextSharp
                byte[] pdfBytes = PdfGenerator.GeneratePdfInMemory(xmlContent);

                // Return PDF as attachment
                return new FileContentResult(pdfBytes, "application/pdf")
                {
                    FileDownloadName = "generated.pdf"
                };
            }
            catch (JsonException ex)
            {
                log.LogError($"JSON parsing error: {ex.Message}");
                return new BadRequestObjectResult(new { error = "Invalid JSON body" });
            }
            catch (Exception ex)
            {
                log.LogError($"Error: {ex.Message}");
                return new ObjectResult(new { error = $"Internal Server Error: {ex.Message}" })
                {
                    StatusCode = 500
                };
            }
        }
    }
}
