#!/usr/bin/perl -w
my $file=shift;
my $type=shift;
open IN,"<$file" or die "$!\n";
while(<IN>)
{
	chomp;
	$_=~s/\s+$//g;
	my @tmp=split /\s+/,$_;
	my $infor=join "\t",@tmp;
	if ($infor =~ /^Sample/ || $infor =~ /^GeneSymbol/)
	{
		print "$infor\ttype\n";
	}else{
		print "$infor\t$type\n";
	}
}
close IN;
