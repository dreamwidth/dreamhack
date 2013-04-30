# database variables for Dreamhacks script
use DBI;

# include the root settings
require '/dreamhack/local/helpers/settings.pl';
my $settings = dh_settings('root');

my $dbserver = "localhost";
my $dbusername = $settings->{'dh_db_readwrite_username'};
my $dbpassword = $settings->{'dh_db_readwrite_password'};
my $dbdatabase = "dreamhacks";

$db = "DBI:mysql:$dbdatabase:$dbserver";
$dbh = DBI->connect($db, $dbusername, $dbpassword);

if ($dbh eq undef) {
  print "<p>Sorry, I couldn't connect to the database for some reason:</p>\n";
  print "<blockquote><i>" . DBI->errstr . "</i></blockquote>";
  exit(0);
}

# other options
$dbh->{'mysql_enable_utf8'} = 1;
$dbh->do("SET NAMES utf8");

return 1;
