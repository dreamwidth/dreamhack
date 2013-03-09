# Hooks for the site scheme(s)
#
# Authors:
#     Janine Costanzo <janine@netrophic.com>
#
# Copyright (c) 2009 by Dreamwidth Studios, LLC.
#
# This program is NOT free software or open-source; you can use it as an
# example of how to implement your own site-specific extensions to the
# Dreamwidth Studios open-source code, but you cannot use it on your site
# or redistribute it, with or without modifications.
#

package DW::Hooks::SiteScheme;

use strict;

LJ::register_hook('nav_links', sub {
    my %opts = @_;

    my $category = $opts{category};

    my $remote = LJ::get_remote();
    my %nav = (
        create => [
            {
                url => "$LJ::SITEROOT/create.bml",
                text => "tropo.nav.create.createaccount",
                loggedin => 0,
                loggedout => 1,
            },
            {
                url => "$LJ::SITEROOT/update.bml",
                text => "tropo.nav.create.updatejournal",
                loggedin => 1,
                loggedout => 0,
            },
            {
                url => "$LJ::SITEROOT/editjournal.bml",
                text => "tropo.nav.create.editjournal",
                loggedin => 1,
                loggedout => 0,
            },
            {
                url => "$LJ::SITEROOT/manage/profile/",
                text => "tropo.nav.create.editprofile",
                loggedin => 1,
                loggedout => 0,
            },
            {
                url => "$LJ::SITEROOT/editpics.bml",
                text => "tropo.nav.create.uploaduserpics",
                loggedin => 1,
                loggedout => 0,
            },
            {
                url => "$LJ::SITEROOT/community/create.bml",
                text => "tropo.nav.create.createcommunity",
                loggedin => 1,
                loggedout => 0,
            },
        ],
        organize => [
            {
                url => "$LJ::SITEROOT/community/manage.bml",
                text => "tropo.nav.organize.managecommunities",
                loggedin => 1,
                loggedout => 0,
            },
            {
                url => "$LJ::SITEROOT/manage/tags.bml",
                text => "tropo.nav.organize.managetags",
                loggedin => 1,
                loggedout => 0,
            },
            {
                url => "$LJ::SITEROOT/friends/edit.bml",
                text => "tropo.nav.organize.managerelationships",
                loggedin => 1,
                loggedout => 0,
            },
            {
                url => "$LJ::SITEROOT/friends/editgroups.bml",
                text => "tropo.nav.organize.managefilters",
                loggedin => 1,
                loggedout => 0,
            },
            {
                url => "$LJ::SITEROOT/manage/settings/",
                text => "tropo.nav.organize.manageaccount",
                loggedin => 1,
                loggedout => 0,
            },
            {
                url => "$LJ::SITEROOT/customize/",
                text => "tropo.nav.organize.selectstyle",
                loggedin => 1,
                loggedout => 0,
            },
            {
                url => "$LJ::SITEROOT/customize/options.bml",
                text => "tropo.nav.organize.customizestyle",
                loggedin => 1,
                loggedout => 0,
            },
        ],
        read => [
            {
                url => $remote ? $remote->journal_base . "/friends" : "",
                text => "tropo.nav.read.readinglist",
                loggedin => 1,
                loggedout => 0,
            },
            {
                url => $remote ? $remote->journal_base . "/friends?show=Y" : "",
                text => "tropo.nav.read.syndicatedfeeds",
                loggedin => 1,
                loggedout => 0,
            },
            {
                url => $remote ? $remote->journal_base . "/tag" : "",
                text => "tropo.nav.read.tags",
                loggedin => 1,
                loggedout => 0,
            },
            {
                url => "$LJ::SITEROOT/tools/recent_comments.bml",
                text => "tropo.nav.read.recentcomments",
                loggedin => 1,
                loggedout => 0,
            },
            {
                url => $remote ? $remote->journal_base . "/profile" : "",
                text => "tropo.nav.read.profile",
                loggedin => 1,
                loggedout => 0,
            },
        ],
        explore => [
            {
                url => "$LJ::SITEROOT/directorysearch.bml",
                text => "tropo.nav.explore.directorysearch",
                loggedin => 1,
                loggedout => 1,
            },
            {
                url => "$LJ::SITEROOT/support/faq.bml",
                text => "tropo.nav.explore.faq",
                loggedin => 1,
                loggedout => 1,
            },
        ],
    );

    if ( $category && $nav{$category} ) {
        return $nav{$category};
    }

    return [];
});

1;
