# This Perl script is designed to be "require"d by whichever script needs it
# Typically this will only be /dreamhacks/lib/dreamhacks-db.pl
# It will put the appropriate settings into %dh_settings, which is shared with read-settings.pl
# NOTE: This script does not parse any escape characters which may exist in the file.

sub dh_settings {
  my ($type) = @_;
  if ($type ne "nonroot" && $type ne "root") { die "Can only load nonroot/root settings"; }
  return dh_load_settings_file("/dreamhack/local/settings.$type");
}

sub dh_load_settings_file {
  my ($settingsfile) = @_;
  my %settings;
  open(my $fh, "<:encoding(ascii)", $settingsfile) || die "Could not open '$settingsfile' for reading: $!";
  while (<$fh>) {
    my $line = $_;
    chomp($line);
    $line=~s/^\s*//;           # remove leading whitespace
    $line=~s/\s*(?:#.*)?$//;   # remove trailing whitespace and comments
    next if ($line eq "");

    my ($name, @value) = split(/=/, $line);
    my $value = join("=", @value);
    $value=~s/^"|"$//g;        # remove any quoting that might be surrounding the value
    $settings{$name} = $value;
  }
  close($fh);
  return \%settings;
}

1;
