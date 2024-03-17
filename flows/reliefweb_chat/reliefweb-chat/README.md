# Introduction

This repo contains a working example of a Reliefweb Situation Report summarization LLM tool, created as part of LLM operationalization workshops. The flow does the following:

1. Parses user request to summarize information, extracts entities needed for querying Reliefweb API
2. Queries ReliefWeb to get situation reports
3. Summarizes the response
4. Extracts refrences
5.  