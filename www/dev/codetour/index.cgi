#!/usr/bin/perl

use CGI qw(:standard);
print header;

use HTML::Entities;
use LWP::Simple qw(get);
use Text::CSV::Slurp;
use IPC::Run3;

my $python = "/usr/bin/python";
my $codetourgenerator = "/dreamhack/lib/bin/codetour.py";

my $dates = param("dates");
my $fromdate = param("fromdate");
my $todate = param("todate");

my $git = '/usr/bin/git --git-dir="/dreamhack/opt/dhroot/.git" --work-tree="/dreamhack/opt/dhroot"';
my ($refreshcommit, $refreshdate) = split(/,/, `$git show -s --pretty=format:"%H,%ci" develop`);
my $codetourrev = `$git rev-parse code-tour`;
my @revs = split(/\n/, `$git log --first-parent --pretty=format:"%H" $codetourrev^..develop`);
# check to see that $codetourrev is the last rev in @revs; if not, that means the 'code-tour' tag isn't on a 'develop' merge and things might be a bit weird.
my $warning = "";
if ($revs[$#revs] eq $codetourrev) {
  $warning = "<p><strong>Warning:</strong> The 'code-tour' tag doesn't seem to be on a commit or merge made directly to 'develop'. You may want to enter the date of the last code tour manually.</p>";
}

my $ctdateunix = `$git show -s --pretty=format:"%ct" code-tour`;
my (undef, undef, undef, $ctday, $ctmonth, $ctyear) = gmtime($ctdateunix);
my $codetourdate = sprintf("%d-%02d-%02d", ($ctyear + 1900), ($ctmonth + 1), $ctday);
# git log --first-parent --oneline code-tour^..develop
if (!defined $dates) {
  print <<HTML;
<html>
<head>
<title>Code Tour Template Generator</title>
<link rel="stylesheet" type="text/css" href="jquery.datepick.css">
<script type="text/javascript" src="jquery.min.js"></script>
<script type="text/javascript" src="jquery.datepick.min.js"></script>
<script type="text/javascript">
\$(function() {
  function selectCustom() {
    \$('#dates-custom').attr('checked', true);
  }
  \$('#popupDatePickerFrom').datepick({dateFormat: 'yyyy-mm-dd', firstDay: 1, onSelect: selectCustom});
  \$('#popupDatePickerTo').datepick(  {dateFormat: 'yyyy-mm-dd', firstDay: 1, onSelect: selectCustom});

  \$('#popupDatePickerFrom, #popupDatePickerTo').change(selectCustom);
});
</script>
<style type="text/css">
  body {
    font-family: 'Arial', sans-serif;
  }

  #calImg {
    display: none;
  }

  .datepick-trigger {
    vertical-align: middle;
  }

  input.date {
    border: 1px solid black;
    margin-top: 5px;
    margin-right: 1px;
    padding: 2px;
  }

  p.defaultnote {
    font-size: smaller;
  }
</style>
</head>
<body>
<h1>Code Tour Generator</h1>
<form method="get" action="index.cgi">
<p>What dates should the code tour cover?</p>
<input type="radio" name="dates" value="fromlasttonow" id="dates-fromlasttonow" checked="true"> <label for="dates-fromlasttonow">From the date of the last code tour (according to the repository: $codetourdate) to now</label><br>$warning
<input type="radio" name="dates" value="custom" id="dates-custom"> <label for="dates-custom">Between these dates:<br><small>(YYYY-MM-DD format, please; click text boxes for date pickers; end date is optional and can be left blank if you don't want an end date.)</small></label><br>
<div id="customDates">
<input type="text" class="date" name="fromdate" id="popupDatePickerFrom" value="$codetourdate"> to <input type="text" class="date" name="todate" placeholder="Now" id="popupDatePickerTo">
</div>
<p><input type="submit" value="Generate"></p>
</form>
<p><small>The default value of the 'from' date is determined by the '<b>code-tour</b>' tag in the local dw-free repository, which is refreshed weekly; the date of the last commit on 'develop' according to this repository is <a href="https://github.com/dreamwidth/dw-free/commit/$refreshcommit">$refreshdate</a>.</small></p>
<p>This script uses <span style='white-space: nowrap;'><a href='http://afuna.dreamwidth.org/profile'><img src='http://s.dreamwidth.org/img/silk/identity/user.png' alt='[personal profile] ' width='17' height='17' style='vertical-align: text-bottom; border: 0; padding-right: 1px;' /></a><a href='http://afuna.dreamwidth.org/'><b>afuna</b></a></span>'s code tour generator, programmed in Python.</p>
</body>
</html>
HTML
}
else {
  my @args = ();
  my $togiven = 0;

  if ($dates eq "fromlasttonow") {
    $fromdate = $codetourdate;
    $todate = "";
  }

  if ($fromdate !~ /^\d\d\d\d-\d\d-\d\d$/) {
    print error("That doesn't look like a valid 'from' date to me. (You entered '$fromdate'). Please try again.");
    exit;
  }
  else {
    push(@args, $fromdate);
  }

  if (($todate ne "") && ($todate !~ /^\d\d\d\d-\d\d-\d\d$/)) {
    print error("That doesn't look like a valid 'to' date to me. (You entered '$todate'). Please try again.");
    exit;
  }
  elsif ($todate ne "") {
    $togiven = 1;
    push(@args, $todate);
  }

  if (($togiven == 1) && ($fromdate gt $todate)) {
    print error("It looks like your 'to' date is before your 'from' date. (You said to search from $fromdate to $todate.) Try again!");
    exit;
  }

  my $dtodate = ($todate == "" ? "now" : $todate);
  my $output, $errors;
  run3([$python, $codetourgenerator, @args], undef, \$output, \$errors);
  my $errno = $?;
  if ($errno == 0) {
    my $doutput = encode_entities($output);
    print <<HTML;
<html>
<head>
<title>Code Tour Template Generator</title>
</head>
<body>
<h2>Resolved issues from $fromdate to $dtodate</h2>
<hr>
<p>Copy and paste the following into a text editor, and then use <a href="http://wiki.dwscoalition.org/notes/How_to_do_a_Code_Tour">the wiki guide</a> to make the code tour. There may be duplicates between this code tour and the last one near the top; you may need to remove them manually. The 'category' field on each issue is set to the milestone if there is one, but for the vast majority this will not be filled in - please edit it if this is the case!</p>
<textarea rows="20" cols="120">$doutput</textarea>
<p>After you're done editing in your external text editor, <a href="http://www.dreamwidth.org/update?usejournal=dw_dev">open a window to post it in dw_dev</a>.</p>
</body>
</html>
HTML
  }
  else {
    my $derrors = encode_entities($errors);
    print <<HTML;
<html>
<head>
<title>Code Tour Template Generator</title>
</head>
<body>
<h2>Failed to get resolved issues from $fromdate to $dtodate</h2>
<hr>
<p>The Python generator returned an error:</p>
<pre>$derrors</pre>
<p>You may want to try again, or else <a href="https://github.com/dreamwidth/dw-free/issues">manually do the code tour</a>. Also, poke <span style='white-space: nowrap;'><a href='http://sophie.dreamwidth.org/profile'><img src='http://s.dreamwidth.org/img/silk/identity/user.png' alt='[personal profile] ' width='17' height='17' style='vertical-align: text-bottom; border: 0; padding-right: 1px;' /></a><a href='http://sophie.dreamwidth.org/'><b>sophie</b></a></span> about this.</p>
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
  function selectCustom() {
    \$('#dates-custom').attr('checked', true);
  }
  \$('#popupDatePickerFrom').datepick({dateFormat: 'yyyy-mm-dd', firstDay: 1, onSelect: selectCustom});
  \$('#popupDatePickerTo').datepick(  {dateFormat: 'yyyy-mm-dd', firstDay: 1, onSelect: selectCustom});

  \$('#popupDatePickerFrom, #popupDatePickerTo').change(selectCustom);
});
</script>
<style type="text/css">
  body {
    font-family: 'Arial', sans-serif;
  }

  #calImg {
    display: none;
  }

  .datepick-trigger {
    vertical-align: middle;
  }

  input.date {
    border: 1px solid black;
    margin-top: 5px;
    margin-right: 1px;
    padding: 2px;
  }

  p.defaultnote {
    font-size: smaller;
  }
</style>
</head>
<body>
<h1>Code Tour Generator - Error</h1>
<p>Sorry, there was an error:</p>
<p><b>$msg</b></p>
<form method="get" action="index.cgi">
<p>What dates should the code tour cover?</p>
<input type="radio" name="dates" value="fromlasttonow" id="dates-fromlasttonow" checked="true"> <label for="dates-fromlasttonow">From the date of the last code tour (according to the repository: $codetourdate) to now</label><br>$warning
<input type="radio" name="dates" value="custom" id="dates-custom"> <label for="dates-custom">Between these dates:<br><small>(YYYY-MM-DD format, please; click text boxes for date pickers; end date is optional and can be left blank if you don't want an end date.)</small></label><br>
<div id="customDates">
<input type="text" class="date" name="fromdate" id="popupDatePickerFrom" value="$codetourdate"> to <input type="text" class="date" name="todate" placeholder="Now" id="popupDatePickerTo">
</div>
<p><input type="submit" value="Generate"></p>
</form>
<p><small>The default value of the 'from' date is determined by the '<b>code-tour</b>' tag in the local dw-free repository, which is refreshed weekly; it was last refreshed at $refreshdate</b>.</small></p>
<p>This script uses <span style='white-space: nowrap;'><a href='http://afuna.dreamwidth.org/profile'><img src='http://s.dreamwidth.org/img/silk/identity/user.png' alt='[personal profile] ' width='17' height='17' style='vertical-align: text-bottom; border: 0; padding-right: 1px;' /></a><a href='http://afuna.dreamwidth.org/'><b>afuna</b></a></span>'s code tour generator, programmed in Python.</p>
</body>
</html>
HTML
}
