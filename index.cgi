#!/usr/bin/perl -w
use warnings;
use strict;

use CGI;
use DBI;
my $cgi = CGI->new();
my $dbh = DBI->connect('DBI:Pg:dbname=scanning;host=localhost',
					   'scanning', 'password')
      or die DBI::errstr;

print $cgi->header();



sub do_import
{
    my $header_printed;

    if (open(my $fh, '-|', '/home/danlyke/scanning/importsetuid'))
    {
        while (my $line = <$fh>)
        {
            unless ($header_printed)
            {
                print "<h2>Importing</h2><ul>";
                $header_printed = 1;
            }
            $line = CGI::escapeHTML($line);
            print "<li>$line</li>\n";
        }
        print "</ul>\n" if $header_printed;
        close $fh;
    }
}

print <<'EOF';
<html>
<head>
<title>Scans</title>

<link rel="stylesheet" type="text/css" href="/scanning/css/jquery.dataTables.css">
<script type="text/javascript" language="javascript" src="/scanning/js/jquery-1.11.1.min.js"></script>
<script type="text/javascript" language="javascript" src="/scanning/js/jquery.dataTables.min.js"></script>
<script type="text/javascript" class="init">

$(document).ready(function() {
$('#example').DataTable();
} );

</script>
</head>
<html>
<h1>Scans</h1>
<form method="POST">
<input name="q" type="text"><input type="submit" name="go" value="search" /> (If you don't see anything, search for blank)
</form>

EOF

do_import();


print <<EOF;
<table id="example" class="display" width="100%" cellspacing="0">
        <thead>
            <tr>
                <th>Image</th>
                <th>Scanned</th>
                <th>Title</th>
                <th>Description</th>
            </tr>
        </thead>
 
        <tfoot>
            <tr>
                <th width="170">Image</th>
                <th width="10em">Scanned</th>
                <th width="20%">Title</th>
                <th>Description</th>
            </tr>
        </tfoot>
<tbody>
EOF

my $sql = 'SELECT * FROM scan';
my $limit;

if ($cgi->param('q'))
{
    my $q = $cgi->param('q');
    my @a = split /\W+/, $q;
    $sql .= " WHERE "
        .join(' AND ',
              map { "(to_tsvector('english',title) @@ to_tsquery('english',"
                        .$dbh->quote($_)
                            .") OR to_tsvector('english',description) @@ to_tsquery('english',"
                        .$dbh->quote($_).'))'
                    } @a
             );
}
elsif (!defined($cgi->param('q')))
{
    $sql .= ' WHERE title IS NULL OR description IS NULL';
}
$sql .= ' ORDER BY entered DESC';


my $sth = $dbh->prepare($sql)
    || die $dbh->errstr;
$sth->execute
    || die $sth->errstr;

while (my $row = $sth->fetchrow_hashref)
{
    print "<tr><td><a href=\"./edit.cgi?id=$row->{id}\"><img src=\"$row->{preview}\" width=\"160\" /></a></td>";
    print "<td>".CGI::escapeHTML($row->{entered});
    print "<br/><a href=\"$row->{filename}\">PDF</a></td>";

    for ('title', 'description')
    {
        my $t = CGI::escapeHTML($row->{$_} // '');
        print "<td>$t</td>"
    }
   
    print "</tr>\n";
}

print <<EOF;
    </tbody>
    </table>
</body>
</html>
EOF
