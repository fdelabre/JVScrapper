use strict;
use warnings;
use LWP::UserAgent;
use HTML::TreeBuilder;
use URI::Escape;

# URL de la page à analyser
my $url = 'https://www.jeuxvideo.com/forums/0-51-0-1-0-1-0-blabla-18-25-ans.htm';

# Création de l'agent utilisateur
my $ua = LWP::UserAgent->new;
$ua->agent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36');

# Envoi de la requête HTTP GET avec l'en-tête d'utilisateur
my $response = $ua->get($url);

if ($response->is_success) {
    my $content = $response->content;

    # Création de l'objet HTML::TreeBuilder
    my $tree = HTML::TreeBuilder->new;
    $tree->parse($content);

    # Recherche des balises <a> avec la classe "topic-title" et stockage des liens et du contenu
    my @topic_titles = $tree->look_down(
        _tag => 'a',
        sub {
            my $class = $_[0]->attr('class') || '';
            return $class =~ /\btopic-title\b/;
        }
    );

    my @links;      # Tableau pour stocker les liens des sujets
    my @contents;   # Tableau pour stocker le contenu des sujets

    print "\n";
    
    # Affichage des balises <a> correspondantes avec leurs numéros
    for (my $i = 0; $i < scalar @topic_titles; $i++) {
        my $topic_title = $topic_titles[$i];
        my $link = $topic_title->attr('href');
        push @links, $link; # Ajout du lien au tableau

        my $text = $topic_title->as_text;
        push @contents, $text; # Ajout du contenu au tableau

        print(($i + 1) . ". $text\n");
    }

    # Demande à l'utilisateur de choisir un sujet
    print "\n";
    print "Ouvrir un sujet [Numéro] : ";
    my $choice = <STDIN>;
    chomp $choice;

    # Vérification de la validité du choix
    if ($choice =~ /^\d+$/ && $choice >= 1 && $choice <= scalar @topic_titles) {
        my $selected_link = $links[$choice - 1];
        my $full_link = 'https://www.jeuxvideo.com' . $selected_link;

        print "Ouverture du lien : $full_link\n";

        # Ouvrir le lien dans le navigateur via la commande shell "xdg-open" (pour Linux)
        system("xdg-open '$full_link'");
    } else {
        print "Choix invalide.\n";
    }

    # Libération de la mémoire utilisée par l'objet HTML::TreeBuilder
    $tree->delete;
} else {
    die "Erreur lors de la requête HTTP: " . $response->status_line;
}