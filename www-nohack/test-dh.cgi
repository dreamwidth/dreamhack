#!/usr/bin/perl

require '/dreamhack/lib/dreamhacks-db-readonly.pl';

# get the hostname we're being called as
my $host = $ENV{'HTTP_HOST'};

# trim the host down to the username and domain
my $nosuchhost = 0;
if (!($host=~s/^.*\.([^.]+\.hack\.dreamwidth\.net)$/$1/i)) { $nosuchhost = 1; }

if (!$nosuchhost) {
  # look this host up in the database
  my $sth = $dbh->prepare("SELECT homedir, apachedir, port FROM users LEFT OUTER JOIN userports USING (`username`) WHERE domain = ?");
  $sth->execute($host);
  if ($sth->rows) {
    my @row = $sth->fetchrow_array();
    # look for PID
    my $pidfile = $row[0] . "/" . $row[1] . "/etc/httpd.pid";
    if (-f $pidfile) {
      # we're running, redirect
#      if ($ENV{'REQUEST_METHOD'} eq "POST") {
#print <<OUT;
#Status: 404 Can't redirect POSTs
#
#Sorry, can't redirect POSTs.
#OUT
#      }
#      else {
        my $uri = $ENV{'REQUEST_URI'};
        my $newurl = "http://127.0.0.1:" . $row[2] . $uri;
        print <<OUT;
Status: 200 OK
Content-Type: text/html
X-REPROXY-URL: $newurl

OUT
#      }
    }
    else {
      # redirect to the 'not on' page
      print <<OUT;
Status: 404 Dreamhack Not On
X-REPROXY-FILE: /dreamhack/www-nohack/no-dreamhack.html

OUT
    }
  }
  else { $nosuchhost = 1; }
}

if ($nosuchhost) {
  # sanitise for display, just in case
  $host=~s/&/&amp;/g;
  $host=~s/</&lt;/g;
  $host=~s/>/&gt;/g;
  print <<OUT;
Status: 404 No Such Host
Content-Type: text/html

<html>
<head>
<title>No Such Host</title>
</head>
<body>
<h1>No Such Host</h1>
<p>The hostname you have given, <b>$host</b>, does not exist on this server.</p>
</body>
</html>
OUT
}
