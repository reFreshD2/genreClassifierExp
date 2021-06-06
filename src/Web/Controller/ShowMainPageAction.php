<?php

declare(strict_types=1);

namespace Genre\Web\Controller;

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Twig\Environment;

class ShowMainPageAction
{
    private Environment $twig;

    public function __construct(Environment $twig)
    {
        $this->twig = $twig;
    }

    public function __invoke(Request $request): Response
    {
        return new Response($this->twig->render('mainPage/index.html.twig'));
    }
}
