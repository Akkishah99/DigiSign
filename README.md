# DigiSign - Azure Function PDF Generator with iTextSharp

A C# Azure Function that generates PDF reports from base64-encoded XML data using the iTextSharp (iText7) library.

## Project Structure

```
DigiSign/
├── PdfGenerator.cs              # Core PDF generation logic (iTextSharp)
├── PdfGeneratorFunction.cs      # Azure Function entry point (HTTP trigger)
├── DigiSign.csproj              # Project configuration & NuGet dependencies
├── Function.json                # Azure Function configuration
├── host.json                    # Azure Functions runtime configuration
├── local.settings.json          # Local development settings
└── .github/workflows/
    └── main_digitalsignas.yml   # GitHub Actions CI/CD pipeline
```

## Key Libraries

- **iText7** (iTextSharp):  Professional PDF generation library for .NET
- **Microsoft.Azure.WebJobs**: Azure Functions runtime
- **Newtonsoft.Json**: JSON parsing for request bodies

## Requirements

- .NET 6.0 or higher
- Azure Functions Core Tools (for local development)
- Visual Studio Code or Visual Studio

## Local Development

### Setup
```bash
cd DigiSign
dotnet restore
```

### Run Locally
```bash
func start
```

### Build
```bash
dotnet build --configuration Release
```

### Publish
```bash
dotnet publish --configuration Release
```

## API Usage

**Endpoint**: `POST /api/GeneratePdf`

**Request Body**:
```json
{
  "signedText": "<base64-encoded-xml-content>"
}
```

**Response**: 
- Success (200): PDF file(s. attachment
- Bad Request (400): `{"error": "error message"}`
- Server Error (500): `{"error": "error message"}`

### Example Request
```bash
curl -X POST https://your-function-app.azurewebsites.net/api/GeneratePdf \
  -H "Content-Type: application/json" \
  -d '{"signedText":"PD94bWwgdmVyc2lvbj0iMS4wIj8+PC9kYXRhPg=="}'
```

## Deployment

Automatic deployment via GitHub Actions:
1. Push to `main` branch
2. GitHub Actions builds and tests
3. Deploys to Azure Function App: `DigitalSignas`

### Manual Deployment
```bash
func azure functionapp publish DigitalSignas
```

## Configuration

Edit `.github/workflows/main_digitalsignas.yml` to change:
- Azure Function App name
- Deployment slot
- .NET version

## License

Confidential - DigiSign Project
