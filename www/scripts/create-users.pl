#!/usr/bin/perl

# alter these variables to alter the characteristics of the created accounts
my $email     = 'youremail@example.invalid';
my $password  = "testpass1";
my $validated = 1;   # validate new accounts automatically? (no email will be sent in either case)

# the next two variables are the percentage chance for each user that it'll grant
# access to or subscribe to any of the users created by this script, including
# itself except where trusting; a user cannot trust themselves. (so a 33% chance
# for $accesschance means that on average, it'll grant access to a third of the
# users created by this script)
my $accesschance    = 33;
my $subscribechance = 33;

# ==============

use strict;
use lib "$ENV{LJHOME}/cgi-bin";
require "ljlib.pl";

my ( $prefix, $num ) = @ARGV;

die "Usage: 'create-users.pl <prefix> <number of users to create>'\neg, 'create-users.pl circletest 100'; this would create circletest1 .. circletest100.\n" unless defined( $num );
die "Second argument must be a number greater than 0, not '$num'.\n" unless $num > 0;
die "Prefix is too long for this many users; please shorten the prefix.\n" if length( $prefix ) + length( $num ) > 25;

my $goodprefix = LJ::canonical_username( $prefix );
die "'$prefix' uses invalid characters; please use another prefix.\n" unless $goodprefix;

print "Creating $num users using prefix '$goodprefix'...\n";

$| = 1;   # disable buffering

for (my $i = 1; $i <= $num; $i++) {
    my $user = $goodprefix . $i;
    LJ::MemCache::delete( 'uidof:' . $user );
    my $u2 = LJ::load_user( $user );
    if ( $u2 ) {
        print "User '$user' already exists, skipping\n";
        next;
    }
    print "Creating '$user'... ";
    my $u = LJ::User->create_personal( user => $user, email => $email, password => $password );
    if ( $u ) {
        print "(userid=" . $u->id . ") ";
        if ( $validated ) {
            print "validating... ";
            LJ::update_user($u, { status => 'A' });
            $u->update_email_alias;
            LJ::run_hook( 'email_verified', $u );
        }
        print "done.\n";
    }
    else {
        die "could not create user! Aborting.\n";
    }
}

print "All users created, creating edges...\n";
for (my $i = 1; $i <= $num; $i++) {
    my $from_user = $goodprefix . $i;
    my $from_u = LJ::load_user( $from_user );
    die "Could not load from_user '$from_user'" unless $from_u;
    for (my $j = 1; $j <= $num; $j++) {
        my $to_user = $goodprefix . $j;
        my $watch = ( ( int( rand( 100 ) ) + 1 ) <= $subscribechance );
        my $trust = ( ( int( rand( 100 ) ) + 1 ) <= $accesschance ) && ( $from_user ne $to_user );
        next unless ( $watch || $trust );   # skip loading the user unless we're actually going to do anything
        my $to_u = LJ::load_user( $to_user );
        die "Could not load to_user '$to_user'" unless $to_u;

        my @actions = ();
        push(@actions, "watch") if $watch;
        push(@actions, "trust") if $trust;
        print "$from_user -> $to_user (" . join(", ", @actions) . ")\n";
        $from_u->add_edge( $to_u, watch => { nonotify => 1 } ) if $watch;
        $from_u->add_edge( $to_u, trust => { nonotify => 1 } ) if $trust;
    }
}

print "All done!\n";

