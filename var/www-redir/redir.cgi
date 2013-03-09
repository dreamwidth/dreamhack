#!/usr/bin/perl

my $host  = $ENV{'HTTP_HOST'};
my $uri   = $ENV{'REQUEST_URI'};

my $result = $host=~s/(\.|^)(?:hack\.dreamwidth\.org|newhack\.dreamwidth\.net)$/$1hack.dreamwidth.net/;
if ($result) {
  print <<REDIR;
Status: 301 Moved Permanently
Location: http://$host$uri

REDIR
}
else {
  print <<OUT;
Content-Type: text/plain; charset=UTF-8

You shouldn't be seeing this. If you do, please contact Sophie on IRC and tell her.

(debug info:)
 Host: $host
  URI: $uri
OUT
}
