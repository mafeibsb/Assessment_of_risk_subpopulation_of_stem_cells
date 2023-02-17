#!/usr/bin/perl -w
use List::Util qw(shuffle);
use Statistics::Descriptive;
use File::Basename;
use Data::Dumper;
my %Cells;
my $subgroup_file=shift;
my $HVG2000_file=shift;
my $GeneExp_file=shift;
my $Sample_name=shift;
my $ratio=shift;
my $outdir=shift;
my $ratio_id=100*$ratio;

my $cluster_id=-1;
my $sample_id=1;
open SF,"<$subgroup_file" or die "$!\n";
while(<SF>)
{
	$_ =~ s/[\r\n]//g;
	$_ =~ s/"//g;
	$_ =~ s/,+$//g;
	my @tmp=split /,/,$_;
	if ($_ =~ /^,/)
	{
		for(my $i=scalar@tmp-1; $i>=0;$i--)
		{
			if($tmp[$i] =~ /cluster/)
			{
				$cluster_id=$i;
			}

			if($tmp[$i] =~ /Sample/)
			{
				$sample_id=$i;
			}
		}
	}else{
		if($tmp[$sample_id] eq $Sample_name)
		{
			my $cell_id=$tmp[0];
			push @{$Cells{$tmp[$sample_id]}{$tmp[$cluster_id]}},$cell_id;
		}
	}
}
close SF;
#print Dumper %Cells;
#die; 
my %Genes;
open HF,"<$HVG2000_file" or die "$!\n";
while(<HF>)
{
	$_ =~ s/[\r\n]//g;
	next if /^""/;
	my $gene=($_ =~ /,/)?(split /,/,$_)[1]:$_;
	$gene=~s/"//g;
	$Genes{$gene}=1;
}
close HF;

foreach my $k(keys %Cells)
{
	my $sub_cells=$Cells{$k};
	my %SelectedCells;
	foreach my $sub_k(keys %$sub_cells)
	{
		my %SelectedCells;
		my %RestCells;
		my @cells;
		# @cells=@{$$sub_cells{$sub_k}};
		foreach my $cell_id(@{$$sub_cells{$sub_k}})
		{
			push @cells, $cell_id;
		}
		@cells=shuffle @cells;
		my $total_cell_num=scalar(@{$$sub_cells{$sub_k}});
		my $select_cell_num=int($total_cell_num*$ratio);
		$select_cell_num=1 if ($select_cell_num == 0);
		for(my $i=0;$i<$select_cell_num;$i++)
		{
			$SelectedCells{$cells[$i]}=$sub_k;
		}
		for(my $i=$select_cell_num;$i<$total_cell_num;$i++)
		{
			$RestCells{$cells[$i]}=$sub_k;
		}

		open $sub_k,">$outdir/$k\_$sub_k\_HVG2000Exp$ratio_id.txt" or die "$!\n";
		my $ratio_id_rest=100-$ratio_id;
		my $rest_k=$sub_k . "RT";
		open $rest_k,">$outdir/$k\_$sub_k\_HVG2000Exp$ratio_id_rest.txt" or die "$!\n";
		open GF,"<$GeneExp_file" or die "$!\n";
		my @selected_cells;
		my @rest_cells;
		while(<GF>)
		{
			$_=~s/[\r\n]//g;
			$_ =~ s/"//g;
			my @tmp=split /,/,$_;
			$tmp[0] ||= 1;
			if ($tmp[0] eq 1)
			{
				print {$sub_k} "GeneSymbol";
				print {$rest_k} "GeneSymbol";
				for (my $i=1;$i<$#tmp;$i++)
				{
					$tmp[$i]=~s/\./-/g;
					if(exists $SelectedCells{$tmp[$i]})
					{
						print {$sub_k} "\t$tmp[$i]";
						push @selected_cells,$i;
					}
					if(exists $RestCells{$tmp[$i]})
					{
						print {$rest_k} "\t$tmp[$i]";
						push @rest_cells,$i;
					}


				}
				print {$sub_k} "\n";
				print {$rest_k} "\n";
			}else{
				if (exists $Genes{$tmp[0]})
				{
					print {$sub_k} "$tmp[0]";
					for (my $i=0;$i<scalar(@selected_cells);$i++)
					{
						my $exp_id=$selected_cells[$i];
						$tmp[$exp_id]=sprintf "%.3f",$tmp[$exp_id];
						print {$sub_k} "\t$tmp[$exp_id]";
					}
					print {$sub_k} "\n";
					
					print {$rest_k} "$tmp[0]";
					for (my $i=0;$i<scalar(@rest_cells);$i++)
					{
						my $exp_id=$rest_cells[$i];
						$tmp[$exp_id]=sprintf "%.3f",$tmp[$exp_id];
						print {$rest_k} "\t$tmp[$exp_id]";
					}
					print {$rest_k} "\n";

				}
			}
		}
		close GF;
		close $sub_k;
		close $rest_k;
	}
}
