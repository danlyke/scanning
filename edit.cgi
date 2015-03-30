#!/usr/bin/perl -w
use warnings;
use strict;

use CGI;
use DBI;
my $cgi = CGI->new();
my $dbh = DBI->connect('DBI:Pg:dbname=scanning;host=localhost',
					   'scanning', 'password')
      or die DBI::errstr;

if ($cgi->param('title')
    || $cgi->param('description'))
{
    print $cgi->header('text/plain');
    if ($cgi->param('id'))
    {
        my $sql = 'UPDATE scan SET '
            .join(', ', map { "$_=".$dbh->quote($cgi->param($_)) } 'title', 'description')
                .' WHERE id='.$cgi->param('id');
        $dbh->do($sql);
        print $sql;
    }
    for ($cgi->param)
    {
        print "$_  ".$cgi->param($_)."\n";
    }
    print $cgi->redirect('./');
}
else
{
    print $cgi->header();
    my $sql = 'SELECT * FROM scan WHERE id='.$dbh->quote($cgi->param('id'));
    my $sth = $dbh->prepare($sql)
        || die $dbh->errstr;
    $sth->execute
        || die $sth->errstr;
    
    print <<'EOF';
<html>
<head>
<title>Edit Scan</title>
</head>
<body>
<h1>Edit Scan</h1>
<form method="post">
EOF

    while (my $row = $sth->fetchrow_hashref)
    {
        print "<img src=\"$row->{preview}\" align=\"left\" />";
        print "<a href=\"$row->{filename}\">PDF</a> ";
        print $cgi->submit("Save Changes");
        print "<br/>";
        print "Title: <br/>";
        print $cgi->hidden('id', $row->{id});
        print $cgi->textfield('title', $row->{title},70);
        print "<br>Description: <br/>\n";
        print $cgi->textarea('description', $row->{description}, 20,80);
    
    }
    
    print <<EOF;
</form>
</body>
</html>
EOF
}


