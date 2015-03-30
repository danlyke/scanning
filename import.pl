#!/usr/bin/perl -w
use warnings;
use strict;
use File::Path qw( make_path ) ;
use autodie qw(:all);

use DBI;

my $inputdir = '/home/brscanner/incoming/';
my @outputdirs = ('/var/www/scanning/files/', '/mnt/int1/scanning/files/');

opendir(my $dh, $inputdir)
    || die "Unable to open $inputdir for reading\n";

my $dbh = DBI->connect('DBI:Pg:dbname=scanning;host=localhost',
					   'scanning', 'password')
    or die $DBI::errstr;

while (my $filename = readdir $dh)
{
    my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) =
        localtime(time);

    my $subdir = sprintf("%04.4d/%02.2d/%02.2d/", $year + 1900, $mon + 1, $mday);

    if ($filename =~ /^(\w+)\.pdf$/i)
    {
        my $outbase = $1;
        for my $outputdir (@outputdirs)
        {
            make_path($outputdir.$subdir);
            system('convert', '-geometry','640x2048', "$inputdir/$filename\[0\]",
                   "$outputdir$subdir$outbase.png");
            system('cp', "$inputdir/$filename", "$outputdir$subdir$outbase.pdf");

            system('chmod', 'a+r', "$outputdir$subdir$outbase.pdf");
            system('chmod', 'a+r', "$outputdir$subdir$outbase.png");
        }
        my $sql = 'INSERT INTO scan(filename, preview) VALUES ('
            .join( ',',
                   map { $dbh->quote("files/$subdir$outbase.$_"); } ('pdf', 'png' )
                 )
                .')';
        $dbh->do($sql) || die $dbh->errstr;
        system('rm', "$inputdir/$filename");
    }
}

closedir $dh;
