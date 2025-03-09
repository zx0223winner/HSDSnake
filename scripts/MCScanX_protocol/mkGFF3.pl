#!/usr/bin/perl -w
if ($#ARGV != 1 ) {
	print "usage: perl mkGFF3.pl <dir to ncbi> <species_folder>\n";
	exit;
}
#use Cwd;
#$path = getcwd();

$path = $ARGV[0];

opendir( DIR, "$path/ncbi/$ARGV[1]" ) || die( "Unable to open $path/ncbi\n" );
@files = readdir( DIR );
foreach $file ( @files ){
	next if( $file !~ /\_genomic\.gff$/ );
	print "$path/ncbi/$ARGV[1]/$file\n";
	open( IN, "<$path/ncbi/$ARGV[1]/$file" ) || die( "Unable to open $path/ncbi/$ARGV[1]/$file\n" );
	@ids = split( /\_/, $file );
	$species = $ids[0];
	while( <IN> ){
		next if( $_ !~ /chromosome\=/i || $_ =~ /chromosome\=Unknown/i );
		@data = split( /\t/, $_ );
		$id = $data[0];
		@data = split( /Name\=/, $_ );
		( $chr = $data[1] ) =~ s/\;.*//;
		$chr =~ s/\W*$//; #chromosome
		#print $_;
		#print "$id*\t$species*\t$chr*\n";
		if( !defined( $tag{ $id } ) ){
			$tag{ $id } = $species.$chr;
		}else{
			print $id, "\t", $tag{ $id }, "\n";
			exit;
		}
	}
	close( IN );

	$file = $species."\_cds\_from\_genomic\.fna";
	print "$path/ncbi/$ARGV[1]/$file\n";
	open( IN, "<$path/ncbi/$ARGV[1]/$file" ) || die( "Unable to open $path/ncbi/$ARGV[1]/$file\n" );
	open( OUT, ">$path/intermediateData/$ARGV[1]/$species.gff" );
	while( <IN> ){
		next if( $_ !~ /^\>/ || $_ !~ /protein_id\=/ );
		#print $_;
		@data = split( /\_cds\_/, $_ );
		( $id = $data[0] ) =~ s/^.*\|//;
		@data = split( /protein_id\=/, $_ );
		( $proteinID = $data[1] ) =~ s/\].*//;
		$proteinID =~ s/\W*$//;	#protein ID
		@locations = split( /location\=/, $data[1] );
		#print "$locations[1]\n\n";
		$locations[1] =~ s/^\D*//;
		$locations[1] =~ s/\D*$//;
		@points = split( /[.,>]+/, $locations[1] );
		#print "$id*\t$proteinID*\t$locations[1]*\n";
		next if( !defined( $tag{ $id } ) );
		print OUT "$tag{ $id }\t$proteinID\t$points[0]\t$points[-1]\n";
	}
	close( IN );
	close( OUT );
}
closedir( DIR );
