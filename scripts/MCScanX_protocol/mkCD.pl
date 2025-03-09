#!/usr/bin/perl -w
#$path = "/storage/ppl/zxwinner/test/DupGen_finder/MCScanX_protocol";
if ($#ARGV != 1 ) {
	print "usage: perl mkCD.pl <dir to ncbi> <species_folder>\n";
	exit;
}
$path = $ARGV[0];

opendir( DIR, "$path/ncbi/$ARGV[1]" ) || die( "Unable to open $path/ncbi/$ARGV[1]\n" );
@files = readdir( DIR );
foreach $file ( @files ){
	next if( $file !~ /\_genomic\.gff$/ );
	print "$path/ncbi/$file\n";
	open( IN, "<$path/ncbi/$ARGV[1]/$file" ) || die( "Unable to open $path/ncbi/$ARGV[1]/$file\n" );
	@ids = split( /\_/, $file );
	$species = $ids[0];
	while( <IN> ){
		next if( $_ !~ /chromosome\=/i || $_ =~ /chromosome\=Unknown/i );
		@data = split( /\t/, $_ );
		$id = $data[0];
		if( !defined( $tag{ $id } ) ){
			$tag{ $id } = 1;
		}else{
			print "Dup for $id in $path/ncbi/$file\n";
			exit;
		}
	}
	close( IN );

	$file = $species."\_cds\_from\_genomic\.fna";
	print "$path/ncbi/$file\n";
	$skip = 0;
	open( IN, "<$path/ncbi/$ARGV[1]/$file" ) || die( "Unable to open $path/ncbi/$ARGV[1]/$file\n" );
	open( OUT, ">$path/intermediateData/$ARGV[1]/$species.cds" );
	while( <IN> ){
		if( $_ !~ /^\>/ ){	#not a header
			next if( $skip );
			print OUT $_;
		}else{	#header
			$skip = 0;
			if( $_ !~ /protein_id\=/ ){
				$skip = 1;
				next;
			}else{
				@data = split( /\_cds\_/, $_ );
				( $id = $data[0] ) =~ s/^.*\|//;
				@data = split( /protein_id\=/, $_ );
				( $proteinID = $data[1] ) =~ s/\].*//;
				$proteinID =~ s/\W*$//;	#protein ID
				if( !defined( $tag{ $id } ) ){
					$skip = 1;
					next;
				}
				print OUT ">$proteinID\n";
			}
		}
	}
	close( IN );
	close( OUT );
}
closedir( DIR );
