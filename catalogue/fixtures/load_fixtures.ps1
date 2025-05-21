# Script PowerShell pour charger les fixtures Django dans l'ordre
$fixtures = @(
    "RoleFixtures.json"
    "UserFixtures.json",
    "RoleUserFixtures.json"
    "TypeFixtures.json",
    "LocalityFixtures.json",
    "TroupeFixtures.json"
    "ArtistFixtures.json",
    "LocationFixtures.json",
    "PriceFixtures.json",
    "ShowFixtures.json",
    "ArtistTypeFixtures.json",
    "ArtistTypeShowFixtures.json",
    "RepresentationFixtures.json",
    "ReviewFixtures.json",
    "ReservationFixtures.json",
    "RepresentationReservationFixtures.json"
)

foreach ($fixture in $fixtures) {
    Write-Host "Chargement de $fixture..."
    # Exécute la commande et attend sa fin avant de continuer
    & python manage.py loaddata $fixture

    if ($LASTEXITCODE -ne 0) {
        Write-Host "Erreur lors du chargement de $fixture. Arret du script." -ForegroundColor Red
        break
    }
}

Write-Host "Chargement termine."
