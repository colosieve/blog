{{- with .File -}}
{{- readFile (path.Join "content" .Path) -}}
{{- end -}}
