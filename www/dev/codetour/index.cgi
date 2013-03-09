#!/usr/bin/perl

use CGI qw(:standard);
print header;

use HTML::Entities;
use LWP::Simple qw(get);
use Text::CSV::Slurp;

my $fromdate = param("fromdate");
if (!defined($fromdate) || ($fromdate eq "")) {
  print <<HTML;
<html>
<head>
<title>Code Tour Template Generator</title>
<link rel="stylesheet" type="text/css" href="jquery.datepick.css">
<script type="text/javascript" src="jquery.min.js"></script>
<script type="text/javascript" src="jquery.datepick.min.js"></script>
<script type="text/javascript">
\$(function() {
  \$('#popupDatePicker').datepick({dateFormat: 'yyyy-mm-dd', firstDay: 1});
});
</script>
</head>
<body>
<form method="get" action="index.cgi">
<p>What date should the code tour start from? (YYYY-MM-DD format, please; click text box for date picker):<br>
<input type="text" name="fromdate" id="popupDatePicker"><br>
<input type="checkbox" name="blankdesc" value="1" id="blankdesc"> <label for="blankdesc">Leave 'description' blank instead of using "FILL IN".<label></p>
<p><input type="submit" value="Generate"></p>
</form>
<p>This script was inspired by, and draws from, <span lj:user='foxfirefey' style='white-space: nowrap;'><a href='http://foxfirefey.dreamwidth.org/profile'><img src='http://s.dreamwidth.org/img/silk/identity/user.png' alt='[personal profile] ' width='17' height='17' style='vertical-align: text-bottom; border: 0; padding-right: 1px;' /></a><a href='http://foxfirefey.dreamwidth.org/'><b>foxfirefey</b></a></span>'s Python code tour generator.</p>
</body>
</html>
HTML
}
else {
  my @now = gmtime();   # this should be okay - it's the same timezone used by Bugzilla.
  my $now = sprintf("%04d-%02d-%02d", $now[5] + 1900, $now[4] + 1, $now[3]);
  if ($fromdate !~ /^\d\d\d\d-\d\d-\d\d$/) {
    print error("That doesn't look like a date to me. (You entered '$fromdate'). Please try again.");
    exit;
  }
  if ($fromdate gt $now) {
    print error("It looks like you're trying to search in the future. (You said $fromdate.) This tool can only search bugs opened in the past. Try again!");
    exit;
  }
  my $url = "http://bugs.dwscoalition.org/buglist.cgi?bug_status=RESOLVED&chfield=bug_status&chfieldfrom=$fromdate&chfieldto=Now&columnlist=bug_severity%2Cpriority%2Cop_sys%2Cassigned_to%2Cbug_status%2Cresolution%2Cshort_desc%2Ccomponent%2Cassigned_to_realname%2Cbug_file_loc&query_format=advanced&resolution=FIXED&ctype=csv&order=changeddate";
  my $durl = encode_entities($url);
  my $manualurl = encode_entities("http://bugs.dwscoalition.org/buglist.cgi?chfieldto=Now&query_format=advanced&chfield=bug_status&chfieldfrom=$fromdate&bug_status=RESOLVED&resolution=FIXED&order=changeddate");

  print <<HTML;
<html>
<head>
<title>Code Tour Template Generator</title>
</head>
<body>
<p>Getting <a href="$durl">the CSV file from Bugzilla</a>...</p>
HTML
  my $csv = get($url);
  if (defined($csv)) {
    print "<p>...got it! Now parsing...</p>\n";
    my $data = Text::CSV::Slurp->load(string => $csv);
    if (defined($data) && (ref($data) eq "ARRAY")) {
      print "<p>Found " . scalar(@{$data}) . " bugs to do!</p>\n";
      my $output = "";
      my $fillin = (defined(param("blankdesc")) && (param("blankdesc") eq "1") ? "" : "FILL IN");
      if (($fillin ne "") && (param("tom") == 1)) { $fillin = "TOM HARDY"; }   # http://dw-dev.dreamwidth.org/105483.html?thread=851467#cmt851467
      foreach my $bug (@{$data}) {
        my $patchby = $bug->{assigned_to_realname};
        if ($patchby=~/\[:([a-zA-Z0-9_]+)\]/) {
          my $user = $1;
          if ($user eq "nobody") {
            $patchby = $fillin;
          }
          else {
            $user=~s/-/_/g;
            $patchby = "<user name=\"" . lc($user) . "\">";
          }
        }
        my $suggby     = "";
        my $reportedby = "";
        my $url = $bug->{bug_file_loc};
        if ($url=~/^http:\/\/dw-suggestions\.dreamwidth\.org\/(\d+\.html$)?/) {
          if ($1) {
            my $fullurl = $url . (index($url, "?") == -1 ? "?" : "&") . "style=site&usescheme=global";
            my $suggestion = get($fullurl);
            my ($sugguser) = $suggestion=~/<span[^>]* lj:user='([^']+)'[^>]* class='ljuser'[^>]*><a href='http:\/\/[^\.]+\.dreamwidth\.org\/profile'><img [^>]+><\/a><a [^>]+><b>[^<]+<\/b><\/a><\/span>\) wrote in/;
            if (defined($sugguser)) { $sugguser=~s/-/_/g; $sugguser = "<user name=\"$sugguser\">"; }
                               else { $sugguser = $fillin; }
            $suggby = "\n<b>Suggested by:</b> $sugguser";
          }
          else {
            $suggby = "\n<b>Suggested by:</b> $fillin";
          }
        }
#        elsif ($url=~/^http:\/\/www\.dreamwidth\.org\/support\/see_request(?:\.bml)?\?id=\d+$/) {
#          my $reqpage = get($url);
#          my ($from, $usertype) = $reqpage=~/<b>From:<\/b><\/td><td><a [^>]+><img [^>]+><\/a><span class='[^']+' [^:]+:user='([^']+)'[^>]+><a [^>]+><img src='http:\/\/s\.dreamwidth\.org\/img\/silk\/identity\/([^.]+)\.png'/;
#          if (!defined($from)) {
#            $from = $fillin;
#          }
#          else {
#            $from = "<user name=\"$from\">";
#          }
#          $reportedby = "\n<b>Reported by:</b> $from";
#        }
        my $desc = $bug->{short_desc};
        $desc=~s/&/&amp;/g;
        $desc=~s/</&lt;/g;
        $desc=~s/>/&gt;/g;
        $output .= <<BUG;
<b><a href="http://bugs.dwscoalition.org/show_bug.cgi?id=$bug->{bug_id}">Bug $bug->{bug_id}</a>:</b> $desc
<b>Category:</b> $bug->{component}$suggby$reportedby
<b>Patch by:</b> $patchby
<b>Description:</b> $fillin

BUG
      }
      $output = encode_entities($output);
      print <<HTML;
<hr>
<p>Copy and paste the following into a text editor, and then use <a href="http://wiki.dwscoalition.org/notes/How_to_do_a_Code_Tour">the wiki guide</a> to make the code tour. Remember that the 'category' and 'patch by' parts are guesses based on the component and assignee fields in Bugzilla; they may not be correct, so please edit them if not!</p>
<p>The code tour includes an automatic "Suggested by:" if the URL on a bug goes to a <span lj:user='dw_suggestions' style='white-space: nowrap;'><a href='http://dw-suggestions.dreamwidth.org/profile'><img src='http://s.dreamwidth.org/img/comm_staff.png' alt='[site community profile] ' width='16' height='16' style='vertical-align: text-bottom; border: 0; padding-right: 1px;' /></a><a href='http://dw-suggestions.dreamwidth.org/'><b>dw_suggestions</b></a></span> post<!--, or an automatic "Reported by:" if the URL goes to a support request-->. The user credited is the person who made the suggestion<!-- or opened the support request-->.</p>
<p>Handy links to all of these bugs can be found on <a href="$manualurl">this Bugzilla page</a>.</p>
<textarea rows="20" cols="120">$output</textarea>
<p>After you're done editing in your external text editor, <a href="http://www.dreamwidth.org/update?usejournal=dw_dev">open a window to post it in dw_dev</a>.</p>
</body>
</html>
HTML
    }
  }
  else {
    print <<HTML;
<p>...but for some reason I couldn't get the file. :(</p>
<p>You may want to try again, or else <a href="$manualurl">manually do the code tour</a>. Also, poke <span lj:user='sophie' style='white-space: nowrap;'><a href='http://sophie.dreamwidth.org/profile'><img src='http://s.dreamwidth.org/img/silk/identity/user.png' alt='[personal profile] ' width='17' height='17' style='vertical-align: text-bottom; border: 0; padding-right: 1px;' /></a><a href='http://sophie.dreamwidth.org/'><b>sophie</b></a></span> about this.</p>
</body>
</html>
HTML
  }
}

sub error {
  my ($msg) = @_;
  return <<HTML;
<html>
<head>
<title>Error - Code Tour Template Generator</title>
<link rel="stylesheet" type="text/css" href="jquery.datepick.css">
<script type="text/javascript" src="jquery.min.js"></script>
<script type="text/javascript" src="jquery.datepick.min.js"></script>
<script type="text/javascript">
\$(function() {
  \$('#popupDatePicker').datepick({dateFormat: 'yyyy-mm-dd', firstDay: 1});
});
</script>
</head>
<body>
<p>Sorry, there was an error:</p>
<p><b>$msg</b></p>
<form method="get" action="index.cgi">
<p>What date should the code tour start from? (YYYY-MM-DD format, please; click text box for date picker):<br>
<input type="text" name="fromdate" id="popupDatePicker"><br>
<input type="checkbox" name="blankdesc" value="1" id="blankdesc"> <label for="blankdesc">Leave 'description' blank instead of using "FILL IN".<label></p>
<p><input type="submit" value="Generate"></p>
</form>
<p>This script was inspired by, and draws from, <span lj:user='foxfirefey' style='white-space: nowrap;'><a href='http://foxfirefey.dreamwidth.org/profile'><img src='http://s.dreamwidth.org/img/silk/identity/user.png' alt='[personal profile] ' width='17' height='17' style='vertical-align: text-bottom; border: 0; padding-right: 1px;' /></a><a href='http://foxfirefey.dreamwidth.org/'><b>foxfirefey</b></a></span>'s Python code tour generator.</p>
</body>
</html>
HTML
}
