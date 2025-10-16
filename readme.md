# Julekort

En enkel webapplikasjon for sending av digitale julekort.

## Utvikling

For automatisk kompilering av SCSS-filer, kjør følgende kommando:

```bash
sass --watch static/scss/:static/css/ --style expanded --no-source-map
```

## Produksjonssetting

For å starte FastAPI-applikasjonen, bruk:

```bash
uvicorn main:app --reload
```
