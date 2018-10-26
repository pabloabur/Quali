add_cus_dep('py','eps', 0, 'py2eps');

sub py2eps{
    my $returnStatus = system("python \"$_[0].py\"");
    die "system() failed with status $rc" unless $returnStatus == 0;
    my $returnStatus = system("inkscape --export-eps=\"$_[0].eps \"$_[0].py\".svg ");
    die "system() failed with status $rc" unless $returnStatus == 0;
}
