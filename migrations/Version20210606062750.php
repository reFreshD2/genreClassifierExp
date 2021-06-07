<?php

declare(strict_types=1);

namespace DoctrineMigrations;

use Doctrine\DBAL\Schema\Schema;
use Doctrine\Migrations\AbstractMigration;

/**
 * Auto-generated Migration: Please modify to your needs!
 */
final class Version20210606062750 extends AbstractMigration
{
    public function getDescription(): string
    {
        return '';
    }

    public function up(Schema $schema): void
    {
        // this up() migration is auto-generated, please modify it to your needs
        $this->addSql('CREATE TABLE music_metrics (id INT AUTO_INCREMENT NOT NULL, min_freq DOUBLE PRECISION NOT NULL, max_freq DOUBLE PRECISION NOT NULL, avg_freq DOUBLE PRECISION NOT NULL, min_amp DOUBLE PRECISION NOT NULL, max_amp DOUBLE PRECISION NOT NULL, avg_amp DOUBLE PRECISION NOT NULL, rhythm INT NOT NULL, rate INT NOT NULL, instruments_sounds_character JSON NOT NULL, music_form VARCHAR(255) NOT NULL, spectral_centroid DOUBLE PRECISION NOT NULL, spectral_roll_of DOUBLE PRECISION NOT NULL, spectral_band_width DOUBLE PRECISION NOT NULL, genre VARCHAR(255) NOT NULL, PRIMARY KEY(id)) DEFAULT CHARACTER SET utf8mb4 COLLATE `utf8mb4_unicode_ci` ENGINE = InnoDB');
    }

    public function down(Schema $schema): void
    {
        // this down() migration is auto-generated, please modify it to your needs
        $this->addSql('DROP TABLE music_metrics');
    }
}
