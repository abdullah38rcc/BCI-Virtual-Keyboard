program graph_apsp;

// Delphi 5 sourcecode for the graph.py python module.
// By leonardo maffi, Version 1.0, April 9 2005
//   This code is for the optional AllPairsShortestPaths method, for the Floyd algorithm.
// If this compiled console program is not accessible, the Graph AllPairsShortestPaths
//   method uses an internal Floyd routine in Python.
// This code can be easely rewritten in C, if needed.


{$APPTYPE CONSOLE}

uses
  SysUtils;
const
  maxint = 2147483647;
type
  TyDist = array of array of integer;
var
  i, j, n, c, r, v, w, d: Integer;
  dist: TyDist;
  line: string;
begin
  Readln(Input, Line);
  n:= length(line);
  SetLength(dist, n, n);
  for j:= 0 to n-1 do
    if line[j+1] = '0'
      then dist[0, j]:= maxint
      else dist[0, j]:= 1;
  for i:= 1 to n-1 do begin
    readln(Input, Line);
    for j:= 0 to n-1 do
      if line[j+1] = '0'
        then dist[i, j]:= maxint
        else dist[i, j]:= 1;
  end;

  (* Python code:
  for i in xrange(n):
    for v in xrange(n):
      for w in xrange(n):
        if dist[v][i] != maxint and dist[i][w] != maxint:
          d = dist[v][i] + dist[i][w]
          if dist[v][w] > d:
            dist[v][w] = d
  *)

  for i:= 0 to n-1 do
    for v:= 0 to n-1 do
      for w:= 0 to n-1 do
        if (dist[v,i] <> maxint) and (dist[i,w] <> maxint) then begin
          d:= dist[v,i] + dist[i,w];
          if dist[v,w] > d then
            dist[v, w]:= d;
        end;

  for c:= 0 to n-1 do begin
    for r:= 0 to n-1 do
      write( dist[r,c], ' ' );
    writeln;
  end;
end.
