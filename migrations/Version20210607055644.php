<?php

declare(strict_types=1);

namespace DoctrineMigrations;

use Doctrine\DBAL\Schema\Schema;
use Doctrine\Migrations\AbstractMigration;

/**
 * Auto-generated Migration: Please modify to your needs!
 */
final class Version20210607055644 extends AbstractMigration
{
    public function getDescription(): string
    {
        return '';
    }

    public function up(Schema $schema): void
    {
        // this up() migration is auto-generated, please modify it to your needs
        $this->addSql('CREATE TABLE audio_file (id INT AUTO_INCREMENT NOT NULL, music_metrics_id INT DEFAULT NULL, path VARCHAR(255) NOT NULL, hash VARCHAR(255) NOT NULL, UNIQUE INDEX UNIQ_C32E2A4C326A6482 (music_metrics_id), PRIMARY KEY(id)) DEFAULT CHARACTER SET utf8mb4 COLLATE `utf8mb4_unicode_ci` ENGINE = InnoDB');
        $this->addSql('ALTER TABLE audio_file ADD CONSTRAINT FK_C32E2A4C326A6482 FOREIGN KEY (music_metrics_id) REFERENCES music_metrics (id)');
        $this->addSql('ALTER TABLE music_metrics ADD audio_file_id INT DEFAULT NULL');
        $this->addSql('ALTER TABLE music_metrics ADD CONSTRAINT FK_E67E389CAC7C70B0 FOREIGN KEY (audio_file_id) REFERENCES audio_file (id)');
        $this->addSql('CREATE UNIQUE INDEX UNIQ_E67E389CAC7C70B0 ON music_metrics (audio_file_id)');
    }

    public function down(Schema $schema): void
    {
        // this down() migration is auto-generated, please modify it to your needs
        $this->addSql('ALTER TABLE music_metrics DROP FOREIGN KEY FK_E67E389CAC7C70B0');
        $this->addSql('DROP TABLE audio_file');
        $this->addSql('DROP INDEX UNIQ_E67E389CAC7C70B0 ON music_metrics');
        $this->addSql('ALTER TABLE music_metrics DROP audio_file_id');
    }
}
